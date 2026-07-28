#!/usr/bin/env python3
"""
网储系统性学习手册 — 章节发布与数据同步脚本
用法：
  python3 scripts/publish_chapter.py <section_id>

示例：
  python3 scripts/publish_chapter.py 01_1_4
"""

import sys
import json
import re
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TOC_PATH = ROOT_DIR / "data" / "toc.json"
INDEX_PATH = ROOT_DIR / "index.html"

def main():
    if len(sys.argv) < 2:
        print("错误: 请提供章节编号 (如 01_1_4)")
        sys.exit(1)

    section_id = sys.argv[1].strip()

    # 1. 读取并更新 data/toc.json
    if not TOC_PATH.exists():
        print(f"错误: 找不到 {TOC_PATH}")
        sys.exit(1)

    with open(TOC_PATH, "r", encoding="utf-8") as f:
        toc_data = json.load(f)

    target_file = None
    target_title = None
    found = False

    for level in toc_data.get("levels", []):
        for chapter in level.get("chapters", []):
            for sec in chapter.get("sections", []):
                if sec.get("id") == section_id:
                    sec["status"] = "available"
                    target_file = sec.get("file")
                    target_title = sec.get("title")
                    level_id = level.get("id")
                    found = True
                    break

    if not found:
        print(f"警告: 未在 toc.json 中找到 ID={section_id}")
    else:
        # 保存更新后的 toc.json
        with open(TOC_PATH, "w", encoding="utf-8") as f:
            json.dump(toc_data, f, ensure_ascii=False, indent=2)
        print(f"✅ 成功更新 data/toc.json: {section_id} -> status='available'")

        # 检查对应 HTML 文件是否存在
        if target_file and level_id:
            html_path = ROOT_DIR / "chapters" / level_id / target_file
            if html_path.exists():
                print(f"✅ 验证文件存在: {html_path.relative_to(ROOT_DIR)}")
            else:
                print(f"⚠️ 警告: 找不到 HTML 文件 {html_path.relative_to(ROOT_DIR)}")

    # 2. 同步更新 index.html 中的 _INLINE_TOC
    if INDEX_PATH.exists():
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            index_content = f.read()

        toc_json_compact = json.dumps(toc_data, ensure_ascii=False, separators=(',', ':'))
        new_inline_line = f"const _INLINE_TOC = {toc_json_compact};"

        # 正则替换 const _INLINE_TOC = {...};
        pattern = r"const _INLINE_TOC = \{.*?\};"
        if re.search(pattern, index_content):
            updated_index = re.sub(pattern, lambda m: new_inline_line, index_content, flags=re.DOTALL)
            with open(INDEX_PATH, "w", encoding="utf-8") as f:
                f.write(updated_index)
            print("✅ 成功同步 index.html 中的 _INLINE_TOC 变量")
        else:
            print("⚠️ 警告: 未在 index.html 中找到 _INLINE_TOC 变量定义")

    # 3. 自动 Git add, commit, push
    commit_msg = f"feat(chapters): publish chapter {section_id}"
    if target_title:
        commit_msg += f" ({target_title})"

    print(f"\n正在提交到 Git 仓库并推送远端...")
    try:
        subprocess.run(["git", "add", "chapters/", "data/toc.json", "index.html", ".nojekyll"], cwd=ROOT_DIR, check=True)
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=ROOT_DIR, check=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=ROOT_DIR, check=True)
        print("🚀 Git 提交与远程 Push 完成！已成功发布至 GitHub Pages。")
    except subprocess.CalledProcessError as e:
        print(f"Git 操作时发生警告/错误: {e}")

if __name__ == "__main__":
    main()
