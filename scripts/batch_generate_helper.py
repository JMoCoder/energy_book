#!/usr/bin/env python3
"""
网储系统性学习手册 — 自动化章节批处理与自包含极致 Prompt 打包生成脚本
用法：
  python3 scripts/batch_generate_helper.py --count 3
  python3 scripts/batch_generate_helper.py --sec 03_1_1
  python3 scripts/batch_generate_helper.py --list
"""

import sys
import json
import argparse
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TOC_PATH = ROOT_DIR / "data" / "toc.json"
PROMPTS_DIR = ROOT_DIR / "documents" / "prompts"
PROMPT_TEMPLATE_PATH = ROOT_DIR / "documents" / "撰写提示词模板.md"
RULES_PATH = ROOT_DIR / "documents" / "写作说明与规范.md"

def load_toc() -> dict:
    if not TOC_PATH.exists():
        print(f"❌ 找不到 TOC 数据文件: {TOC_PATH}")
        sys.exit(1)
    with open(TOC_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_pending_sections(toc_data: dict, count: int = None, target_sec_id: str = None) -> list[dict]:
    pending = []
    for level in toc_data.get("levels", []):
        level_id = level.get("id", "")
        level_title = level.get("title", "")
        for chapter in level.get("chapters", []):
            chap_title = chapter.get("title", "")
            for sec in chapter.get("sections", []):
                sec_id = sec.get("id")
                sec_status = sec.get("status", "draft")
                sec_info = {
                    "sec": sec,
                    "level_id": level_id,
                    "level_title": level_title,
                    "chap_title": chap_title,
                    "target_file": ROOT_DIR / "chapters" / level_id / sec.get("file", "")
                }
                
                if target_sec_id:
                    if sec_id == target_sec_id:
                        pending.append(sec_info)
                        return pending
                else:
                    if sec_status != "available":
                        pending.append(sec_info)
                        if count and len(pending) >= count:
                            return pending
    return pending

def run_create_chapter(sec_id: str) -> bool:
    print(f"🛠️  [阶段 1] 运行脚手架生成器: create_chapter.py {sec_id}")
    cmd = [sys.executable, str(ROOT_DIR / "scripts" / "create_chapter.py"), sec_id]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"   ✅ DOM 脚手架初始化完成")
        return True
    else:
        print(f"   ❌ 脚手架创建失败: {result.stderr}")
        return False

def build_deep_prompt(sec_info: dict) -> str:
    """提取全量写作铁律与模板，合成自包含（Self-contained）的极致 Prompt"""
    sec = sec_info["sec"]
    sec_id = sec["id"]
    sec_title = sec["title"]
    level_id = sec_info["level_id"]
    level_title = sec_info["level_title"]
    chap_title = sec_info["chap_title"]
    file_rel_path = f"chapters/{level_id}/{sec['file']}"
    abs_html_path = ROOT_DIR / "chapters" / level_id / sec["file"]

    template_content = ""
    if PROMPT_TEMPLATE_PATH.exists():
        template_content = PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")

    prompt_content = f"""# 《中国网储系统性学习手册》最高标准撰写任务：章节 `{sec_id}` ({sec_title})

> **【重要】上下文隔离与质量铁律**：你当前处于一个**全新的、独立的上下文窗口**中。本 Prompt 包含了撰写本章节所需的全部规范、铁律与元数据。请发挥最高水准，撰写一份**丰满、深刻、讲透**的独立 HTML 章节。

---

## 【撰写提示词模板全文（规范上下文注入）】

{template_content}

---

## 一、章节元数据与定位

- **章节编号**：`{sec_id}`
- **章节标题**：`{sec_title}`
- **所属层级**：`{level_id}` ({level_title})
- **所属大章**：`{chap_title}`
- **目标 HTML 文件路径**：`{abs_html_path}` (相对路径: `{file_rel_path}`)
- **正文字数硬性目标**：**`<main class="chapter-content">` 正文节点内纯中文汉字不少于 6,000 字，上不封顶！**（不含 HTML 标签、CSS 样式、MathJax 代码与测验区，以“完全讲透”为评估标准，充分展开每一个历史背景、政策制度、技术机制与工程细节）。

---

## 二、最高优先级：深入浅出写作铁律（必须严格执行）

### 1. 场景引入 (200-400 字)
- **绝对禁止**使用“本节将介绍……”、“本章主要学习……”等教科书式枯燥开头。
- **必须**使用一个具体的、有画面感的**历史真实事件/工程现场告警/重大政策博弈痛点**切入，引发读者的强烈好奇心。

### 2. 核心正文：三层递进（每个概念必须透彻）
每引入任何一个新概念、新政策或新技术，必须执行以下三层递进：
1. **第一层（直觉感受）**：用一句零专业词汇的“大白话”点明它是什么。
2. **第二层（生活类比）**：用生活日常场景进行类比，且类比必须**完整闭环**（类比里的每个元素必须一一对应回物理/体制机制）。必须使用包含如下 DOM 结构的组件：
   ```html
   <div class="callout callout-analogy">
       <div class="callout-header"><span class="callout-icon">🔍</span>生活类比：[类比名称]</div>
       <div class="callout-body">
           <p>[完整闭环的类比阐述...]</p>
       </div>
   </div>
   ```
3. **第三层（工程/政策意义）**：解释其在实际储能与电力系统里的工程作用或经济影响，必须结合**中国真实项目、具体政策文号或 MW/MWh 级实测数据**（使用 `callout-case` 卡片）。

### 3. 公式与专业词汇使用原则
- **专业词汇**首次出现时必须附带中英文全称：`储能变流器（Power Conversion System，PCS）`，后文方可直接用缩写。
- **公式控制**：切勿孤立抛出公式或堆砌变形公式，每个公式前须有文字铺垫，后须紧跟工程含义解读。

---

## 三、HTML 节点与样式组件规范

请直接在脚手架 HTML 文件（`{file_rel_path}`）中进行充实，必须保留并丰富以下节点：

1. **学习目标 (`<section class="learning-goals">`)**：3-5 条明确的学习目标。
2. **场景引入 (`<section class="scene-intro">`)**：具体有代入感的工程/历史场景。
3. **正文内容 (`<main class="chapter-content">`)**：2-6 个层层递进的 H2 模块，插入 `callout-analogy`, `callout-case`, `callout-tips`, `callout-warning` 等丰富卡片。
4. **本节小结 (`<section class="chapter-summary">`)**：3-5 条精炼复盘。
5. **知识测验 (`<section class="quiz-section">`)**：
   - **5 道深度单选题**（严禁出纯数值计算题，必须考察概念理解与辨析）。
   - 每题包含 `<div class="quiz-answer" id="qX-answer" style="display:none">`。
   - **每题解析不少于 100-150 字**，必须详细阐述为什么正确答案是对的，以及**为什么其他三个选项是错的**。
   - 保留 `<button class="btn-check-answer" onclick="checkAnswers()">` 与 `<p class="quiz-score" id="score-display"></p>`。
6. **章节底部导航与相关章节 (`<nav class="bottom-nav">` 与 `<section class="cross-refs">`)**：保留并更新前后相邻章节链接。

---

## 四、自查与硬性门禁（完成后的验证命令）

正文填充完成后，请在终端运行以下校验脚本，确保通过所有硬性质量门禁：

```bash
python3 scripts/validate_chapter.py {sec_id}
python3 scripts/publish_chapter.py {sec_id}
```

**现在，请按照以上最高标准，直接为 `{file_rel_path}` 编写正文！**
"""
    return prompt_content
    return prompt_content

def generate_isolated_prompt_file(sec_info: dict) -> Path:
    PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
    sec_id = sec_info["sec"]["id"]
    prompt_file = PROMPTS_DIR / f"prompt_{sec_id}.md"
    content = build_deep_prompt(sec_info)
    prompt_file.write_text(content, encoding="utf-8")
    return prompt_file

def main():
    parser = argparse.ArgumentParser(description="网储手册自动化章节批处理与自包含 Prompt 导出工具")
    parser.add_argument("-n", "--count", type=int, help="设定需要批量准备的未完成章节数量 (如: 3)")
    parser.add_argument("-s", "--sec", type=str, help="指定生成的章节 ID (如: 03_1_1)")
    parser.add_argument("-l", "--list", action="store_true", help="列出后续未完成的章节队列")
    
    args = parser.parse_args()
    toc_data = load_toc()

    if args.list:
        pending = get_pending_sections(toc_data, count=20)
        print(f"📋 当前待撰写章节队列 (前 {len(pending)} 篇):")
        for p in pending:
            print(f"  • {p['sec']['id']} — {p['sec']['title']} (层级: {p['level_id']})")
        return

    if not args.count and not args.sec:
        print("💡 未指定参数，默认准备接下来 1 篇未完成章节。可以使用 --count N 或 --sec XX_X_X。")
        args.count = 1

    pending_secs = get_pending_sections(toc_data, count=args.count, target_sec_id=args.sec)
    
    if not pending_secs:
        print("🎉 完美！没有找到符合条件的未完成章节。")
        return

    print(f"🚀 [流水线已启动] 正在为 {len(pending_secs)} 个章节准备脚手架与独立极致 Prompt：\n")
    
    for idx, item in enumerate(pending_secs, 1):
        sec_id = item["sec"]["id"]
        sec_title = item["sec"]["title"]
        print(f"==================================================")
        print(f"📌 [{idx}/{len(pending_secs)}] 准备章节: {sec_id} — {sec_title}")
        print(f"==================================================")
        
        # 1. 自动生成脚手架
        run_create_chapter(sec_id)
        
        # 2. 生成自包含极致 Prompt 文件
        prompt_path = generate_isolated_prompt_file(item)
        print(f"📄 [独立 Prompt 包已就绪]:")
        print(f"   --> file://{prompt_path}\n")

    print("==================================================")
    print("✨ 自动化批处理准备完成！")
    print("👉 标准独立窗口写作 SOP:")
    print("   1. 打开生成的 `documents/prompts/prompt_XX_X_X.md` 文件。")
    print("   2. 全选复制内容，在新 Context 窗口（或纯净 AI 对话框）中粘贴发送。")
    print("   3. 生成完成后，运行 `python3 scripts/validate_chapter.py XX_X_X` 开启硬性校验！")

if __name__ == "__main__":
    main()
