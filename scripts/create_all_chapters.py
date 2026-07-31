#!/usr/bin/env python3
"""
中国网储系统性学习手册 — 为 toc.json 中全部缺失章节生成 HTML 骨架脚本
用法：
  python3 scripts/create_all_chapters.py
"""

import json
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TOC_PATH = ROOT_DIR / "data" / "toc.json"
CREATE_SCRIPT = ROOT_DIR / "scripts" / "create_chapter.py"

def main():
    if not TOC_PATH.exists():
        print(f"❌ 错误: 找不到 {TOC_PATH}")
        return

    with open(TOC_PATH, "r", encoding="utf-8") as f:
        toc = json.load(f)

    all_section_ids = []
    for level in toc.get("levels", []):
        for ch in level.get("chapters", []):
            for sec in ch.get("sections", []):
                all_section_ids.append(sec["id"])

    print(f"🔍 检查 toc.json 中全部 {len(all_section_ids)} 个章节...")

    created_count = 0
    existing_count = 0

    for sec_id in all_section_ids:
        cmd = ["python3", str(CREATE_SCRIPT), sec_id]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if "已存在" in res.stdout:
            existing_count += 1
        elif res.returncode == 0:
            created_count += 1
            print(f"✅ 生成新章节骨架: {sec_id}")
        else:
            print(f"❌ 生成章节 {sec_id} 失败: {res.stderr}")

    print(f"\n🎉 处理完毕！已有章节: {existing_count} 章，新建骨架: {created_count} 章。")

if __name__ == "__main__":
    main()
