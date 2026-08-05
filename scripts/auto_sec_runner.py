#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网储系统性学习手册 — 全自动多智能体 SEC 链式写作调度器 (v1.0)
特点：利用 agy CLI 独立进程，确保每一个章节都在全新的上下文窗口（0历史负担）中撰写。
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TOC_PATH = ROOT_DIR / "data" / "toc.json"
AGY_BIN = "/home/jiamoo/.local/bin/agy"
HELPER_SCRIPT = ROOT_DIR / "scripts" / "batch_generate_helper.py"
VALIDATE_SCRIPT = ROOT_DIR / "scripts" / "validate_chapter.py"
PROMPT_TEMPLATE_PATH = ROOT_DIR / "documents" / "撰写提示词模板.md"

def get_all_sections():
    """从 toc.json 中获取所有章节列表及状态"""
    if not TOC_PATH.exists():
        print(f"❌ 错误: 找不到 {TOC_PATH}")
        return []
    
    with open(TOC_PATH, "r", encoding="utf-8") as f:
        toc = json.load(f)

    sections = []
    for level in toc.get("levels", []):
        level_id = level.get("id")
        level_title = level.get("title", "")
        for chapter in level.get("chapters", []):
            chap_title = chapter.get("title", "")
            for sec in chapter.get("sections", []):
                sections.append({
                    "id": sec.get("id"),
                    "title": sec.get("title"),
                    "file": sec.get("file"),
                    "status": sec.get("status", "draft"),
                    "level_id": level_id,
                    "level_title": level_title,
                    "chap_title": chap_title,
                    "abs_file_path": str(ROOT_DIR / "chapters" / level_id / sec.get("file"))
                })
    return sections

def update_section_status(section_id, new_status="available"):
    """更新 toc.json 中特定章节的状态"""
    if not TOC_PATH.exists():
        return False
    with open(TOC_PATH, "r", encoding="utf-8") as f:
        toc = json.load(f)

    updated = False
    for level in toc.get("levels", []):
        for chapter in level.get("chapters", []):
            for sec in chapter.get("sections", []):
                if sec.get("id") == section_id:
                    sec["status"] = new_status
                    updated = True
                    break

    if updated:
        with open(TOC_PATH, "w", encoding="utf-8") as f:
            json.dump(toc, f, ensure_ascii=False, indent=2)
        print(f"✅ [状态机更新] 章节 {section_id} 状态已更新为 '{new_status}'")
    return updated

def get_next_target(target_sec_id=None):
    """获取下一个待撰写的章节"""
    sections = get_all_sections()
    if target_sec_id:
        for sec in sections:
            if sec["id"] == target_sec_id:
                return sec
        return None
    
    for sec in sections:
        if sec["status"] in ["draft", "pending"]:
            return sec
    return None

def run_single_sec(sec_info, max_retries=3):
    """为单个章节启动全新的 agy CLI 智能体进程"""
    sec_id = sec_info["id"]
    sec_title = sec_info["title"]

    # 1. 确保脚手架与独立 Deep Prompt 已就绪
    print(f"\n🛠️  [阶段 1] 正在为 {sec_id} 准备自包含 Deep Prompt...")
    prep_res = subprocess.run([sys.executable, str(HELPER_SCRIPT), "--sec", sec_id], capture_output=True, text=True)
    if prep_res.returncode != 0:
        print(f"❌ 准备 Deep Prompt 失败: {prep_res.stderr}")
        return False

    prompt_path = ROOT_DIR / "documents" / "prompts" / f"prompt_{sec_id}.md"
    if not prompt_path.exists():
        print(f"❌ 找不到生成的 Prompt 文件: {prompt_path}")
        return False

    # 2. 读取《撰写提示词模板.md》全文作为标准规范上下文注入
    template_text = ""
    if PROMPT_TEMPLATE_PATH.exists():
        template_text = PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")

    # 3. 构建传递给独立 agy 进程的 Prompt
    agent_prompt = f"""你是一个顶级的电力系统与电池储能专家工程写作智能体。

【最高控制指令及规范模板（直接注入）】：
{template_text}

---

【当前写作目标与硬性执行任务】：
目标章节：【{sec_id} — {sec_title}】
所属层级：{sec_info['level_id']} ({sec_info['level_title']}) / {sec_info['chap_title']}
目标文件路径：{sec_info['abs_file_path']}
独立 Prompt 路径：{prompt_path}

【硬性执行步骤】：
1. 用 view_file 仔细阅读 {prompt_path} 中的全部写作规范、大纲结构与 H2 序号连续性约束。
2. 按照《撰写提示词模板》与 {prompt_path}，撰写【{sec_title}】的完整 HTML 内容，直接覆盖写入到目标文件：{sec_info['abs_file_path']}。
3. **字数与讲透要求**：必须根据提示词大纲，沿着 H2 标题（一、二、三...）逐步深入剖析，确保 <main class="chapter-content"> 内的纯中文汉字数达到 6,000 字以上！严禁盲目拼凑段落，严禁 H2 标题序号乱序！
4. 撰写并落盘完成后，在终端运行：python3 {VALIDATE_SCRIPT} {sec_id}
5. 如果校验未通过，仔细阅读报错信息，使用 replace_file_content 修正 HTML 内容，直到 validate_chapter.py 打印【✅ 所有规范校验通过！】且退出码为 0。

请立即启动并完成本节撰写与校验！"""

    cmd = [
        AGY_BIN,
        "--dangerously-skip-permissions",
        "--print-timeout", "30m",
        "--print",
        agent_prompt
    ]

    print("\n" + "=" * 65)
    print(f"🚀 [全新智能体进程启动] 目标: {sec_id} — {sec_title} (0历史包袱)")
    print("=" * 65 + "\n")

    for attempt in range(1, max_retries + 1):
        print(f"👉 尝试第 {attempt}/{max_retries} 次启动独立 agy Agent 进程...")
        start_time = time.time()

        res = subprocess.run(cmd, cwd=str(ROOT_DIR), capture_output=False)
        elapsed = time.time() - start_time
        print(f"\n⏱️ 智能体进程执行结束 (耗时: {elapsed:.1f} 秒)")

        # 3. 运行质量门禁校验
        val_res = subprocess.run([sys.executable, str(VALIDATE_SCRIPT), sec_id], capture_output=True, text=True)
        if val_res.returncode == 0:
            print(f"\n🎉 [质量门禁 PASS] 章节 {sec_id} 成功通过 validate_chapter.py 校验！")
            update_section_status(sec_id, "available")
            return True
        else:
            sleep_sec = 10 * attempt
            print(f"\n⚠️ [校验未通过] 章节 {sec_id} 门禁结果:\n{val_res.stdout}\n{val_res.stderr}")
            print(f"等待 {sleep_sec} 秒后重试 ({attempt}/{max_retries})...")
            time.sleep(sleep_sec)

    print(f"❌ [失败] 章节 {sec_id} 在 {max_retries} 次尝试后仍未通过硬性质量门禁。")
    return False

def main():
    max_secs = 1
    target_sec_id = None

    if len(sys.argv) > 1:
        arg = sys.argv[1].strip()
        if arg.isdigit():
            max_secs = int(arg)
        else:
            target_sec_id = arg

    print("==========================================================")
    print(" ⚡ 网储系统性学习手册 — 全自动多智能体 SEC 链式调度器启动 ")
    print("==========================================================")

    completed_count = 0
    while completed_count < max_secs:
        sec_info = get_next_target(target_sec_id)
        if not sec_info:
            print("🏁 所有章节已全部完成，或没有找到待撰写的草稿章节！")
            break

        success = run_single_sec(sec_info)
        if not success:
            print(f"🛑 自动化链式调度暂停：章节 {sec_info['id']} 未能成功交付。请排查原因。")
            break

        completed_count += 1
        if target_sec_id:
            break

        if completed_count < max_secs:
            print(f"\n🎉 已完成 {completed_count}/{max_secs} 节！等待 3 秒后启动下一个全新智能体...\n")
            time.sleep(3)

    print(f"\n🏁 调度结束！本次调度共完成 {completed_count} 节写作。")

if __name__ == "__main__":
    main()
