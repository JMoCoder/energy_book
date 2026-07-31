#!/usr/bin/env python3
"""
中国网储系统性学习手册 — 分板块与全本 EPUB 电子书自动构建脚本
用法：
  python3 scripts/build_epub.py              # 构建所有可用板块 EPUB 及全本 EPUB
  python3 scripts/build_epub.py --module L1  # 仅构建指定板块 (如 L0, L1, SP4...)
  python3 scripts/build_epub.py --full-only # 仅构建全本合并 EPUB
"""

import sys
import os
import re
import json
import argparse
import subprocess
import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TOC_PATH = ROOT_DIR / "data" / "toc.json"
CSS_PATH = ROOT_DIR / "assets" / "css" / "main.css"
OUTPUT_DIR = ROOT_DIR / "documents" / "epub"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

LEVEL_CODE_MAP = {
    "level_00": "L0",
    "level_01": "L1",
    "level_02": "L2",
    "level_03": "L3",
    "level_04": "L4",
    "level_05": "L5",
    "level_06": "L6",
    "level_07": "L7",
    "level_08": "L8",
    "sp_01": "SP1",
    "sp_02": "SP2",
    "sp_03": "SP3",
    "sp_04": "SP4",
    "sp_05": "SP5",
    "sp_06": "SP6",
}

# EPUB 专属增强 CSS 样式
EPUB_CUSTOM_CSS = """
/* ================================================================
   EPUB 电子书专属排版微调
   ================================================================ */
@page {
  margin: 15pt;
}
body {
  font-family: "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
  line-height: 1.6;
  color: #1A1A2E;
  background-color: #FFFFFF;
}
.top-nav, .bottom-nav, .cross-refs, .chapter-footer, .btn-back-top, .btn-check-answer {
  display: none !important;
}
.quiz-answer {
  display: block !important;
  margin-top: 12px !important;
  padding: 12px 16px !important;
  background-color: #F0FDF4 !important;
  border-left: 4px solid #059669 !important;
  border-radius: 4px !important;
}
.epub-title-page {
  text-align: center;
  padding: 80px 20px 40px 20px;
  page-break-after: always;
}
.book-main-title {
  font-size: 2.2em;
  color: #1A5F96;
  margin-bottom: 0.3em;
  font-weight: bold;
}
.book-sub-title {
  font-size: 1.4em;
  color: #4A5568;
  margin-bottom: 1.5em;
}
.book-meta {
  font-size: 0.9em;
  color: #718096;
}
.epub-chapter {
  page-break-before: always;
  break-before: page;
  padding-top: 10px;
}
.callout {
  margin: 1.5em 0;
  padding: 12px 16px;
  border-left: 4px solid #1A5F96;
  background-color: #F0F7FF;
  border-radius: 4px;
}
.callout-analogy {
  border-left-color: #0A8A5F;
  background-color: #ECFDF5;
}
.callout-warning {
  border-left-color: #D97706;
  background-color: #FFFBEB;
}
.callout-danger {
  border-left-color: #DC2626;
  background-color: #FEF2F2;
}
.data-table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5em 0;
  font-size: 0.9em;
}
.data-table th, .data-table td {
  border: 1px solid #CBD5E1;
  padding: 8px 10px;
}
.data-table th {
  background-color: #F1F5F9;
  font-weight: bold;
}
"""

def load_toc():
    if not TOC_PATH.exists():
        print(f"❌ 错误: 找不到目录索引 {TOC_PATH}")
        sys.exit(1)
    with open(TOC_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def load_css():
    main_css = ""
    if CSS_PATH.exists():
        with open(CSS_PATH, "r", encoding="utf-8") as f:
            main_css = f.read()
    return main_css + "\n" + EPUB_CUSTOM_CSS

def clean_chapter_html(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    # 提取 page-wrapper 内容
    wrapper_match = re.search(r'<div class="page-wrapper">(.*?)</div>\s*<!--\s*end page-wrapper\s*-->', html, re.DOTALL)
    if not wrapper_match:
        wrapper_match = re.search(r'<div class="page-wrapper">(.*?)</div>\s*<button id="btnBackTop"', html, re.DOTALL)
    if not wrapper_match:
        wrapper_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
    
    content = wrapper_match.group(1) if wrapper_match else html

    # 剔除网页导航、脚标及交互脚本
    content = re.sub(r'<nav class="top-nav".*?</nav>', '', content, flags=re.DOTALL)
    content = re.sub(r'<nav class="bottom-nav".*?</nav>', '', content, flags=re.DOTALL)
    content = re.sub(r'<section class="cross-refs".*?</section>', '', content, flags=re.DOTALL)
    content = re.sub(r'<footer class="chapter-footer".*?</footer>', '', content, flags=re.DOTALL)
    content = re.sub(r'<button id="btnBackTop".*?</button>', '', content, flags=re.DOTALL)
    content = re.sub(r'<button class="btn-check-answer".*?</button>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script.*?</script>', '', content, flags=re.DOTALL)

    # 静态展示测验解析答案
    content = re.sub(r'style="display:\s*none;?"', 'style="display:block;"', content)

    return content.strip()

def collect_module_sections(level_info):
    lid = level_info["id"]
    dir_path = ROOT_DIR / "chapters" / lid
    if not dir_path.exists():
        return []

    sections = []
    for ch in level_info.get("chapters", []):
        for sec in ch.get("sections", []):
            sec_file = sec.get("file")
            if sec_file:
                fp = dir_path / sec_file
                if fp.exists():
                    sections.append((sec.get("id"), sec.get("title"), fp))

    if not sections and dir_path.exists():
        for f in sorted(os.listdir(dir_path)):
            if f.endswith(".html"):
                fp = dir_path / f
                sections.append((f.replace(".html", ""), f, fp))

    return sections

def build_epub_file(title, author, html_content, output_epub_path):
    build_dir = OUTPUT_DIR / "_build_tmp"
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir(parents=True, exist_ok=True)

    content_html_path = build_dir / "index.html"
    with open(content_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    cmd = [
        "ebook-convert",
        str(content_html_path),
        str(output_epub_path),
        "--title", title,
        "--authors", author,
        "--publisher", "中国网储系统性学习手册团队",
        "--language", "zh",
        "--level1-toc", "//h:h1",
        "--level2-toc", "//h:h2",
        "--level3-toc", "//h:h3",
        "--chapter", "//h:h1",
        "--epub-inline-toc",
        "--dont-split-on-page-breaks"
    ]

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    shutil.rmtree(build_dir, ignore_errors=True)

    if res.returncode == 0 and output_epub_path.exists():
        size_mb = output_epub_path.stat().st_size / (1024 * 1024)
        print(f"✅ [成功] {output_epub_path.name} ({size_mb:.2f} MB)")
        return True
    else:
        print(f"❌ [失败] {output_epub_path.name}: {res.stderr}")
        return False

def build_single_module(level_info, combined_css):
    lid = level_info["id"]
    ltitle = level_info["title"]
    code = LEVEL_CODE_MAP.get(lid, lid.upper())
    sections = collect_module_sections(level_info)

    if not sections:
        print(f"⏩ [跳过] {code} ({ltitle}): 无已编写章节")
        return None

    print(f"\n📦 正在构建板块 EPUB: {code} - {ltitle} (含 {len(sections)} 章)...")

    html_parts = [f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>中国网储系统性学习手册 · {code} {ltitle}</title>
  <style>
  {combined_css}
  </style>
</head>
<body>
  <div class="epub-title-page">
    <h1 class="book-main-title">中国网储系统性学习手册</h1>
    <h2 class="book-sub-title">{code}：{ltitle}</h2>
    <p class="book-meta">板块编号：{code} | 收录章节：{len(sections)} 章</p>
  </div>
"""]

    for sec_id, sec_title, fp in sections:
        body = clean_chapter_html(fp)
        html_parts.append(f'<div class="epub-chapter" id="sec_{sec_id}">\n{body}\n</div>\n')

    html_parts.append("</body>\n</html>")
    full_html = "\n".join(html_parts)

    out_name = f"{code}_{ltitle}.epub"
    out_path = OUTPUT_DIR / out_name
    success = build_epub_file(
        title=f"网储系统性学习手册 - {code} {ltitle}",
        author="中国网储系统性学习手册",
        html_content=full_html,
        output_epub_path=out_path
    )
    return out_path if success else None

def build_full_book(toc_data, combined_css):
    print("\n📚 正在合并全本 EPUB (包含所有已出版板块章节)...")
    all_module_sections = []
    total_chapters = 0

    for level in toc_data.get("levels", []):
        lid = level["id"]
        ltitle = level["title"]
        code = LEVEL_CODE_MAP.get(lid, lid.upper())
        secs = collect_module_sections(level)
        if secs:
            all_module_sections.append((code, ltitle, secs))
            total_chapters += len(secs)

    if not all_module_sections:
        print("❌ 未找到可用的章节内容，无法构建全本")
        return None

    html_parts = [f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>中国网储系统性学习手册 · 全本</title>
  <style>
  {combined_css}
  </style>
</head>
<body>
  <div class="epub-title-page">
    <h1 class="book-main-title">中国网储系统性学习手册</h1>
    <h2 class="book-sub-title">系统性全本 (包含八大 LEVEL 与 SP 专题板块)</h2>
    <p class="book-meta">全书已收录 {len(all_module_sections)} 大板块，共 {total_chapters} 核心章节</p>
  </div>
"""]

    for code, ltitle, secs in all_module_sections:
        for sec_id, sec_title, fp in secs:
            body = clean_chapter_html(fp)
            html_parts.append(f'<div class="epub-chapter" id="sec_{sec_id}">\n{body}\n</div>\n')

    html_parts.append("</body>\n</html>")
    full_html = "\n".join(html_parts)

    out_path = OUTPUT_DIR / "中国网储系统性学习手册_全本.epub"
    success = build_epub_file(
        title="中国网储系统性学习手册 (全本)",
        author="中国网储系统性学习手册",
        html_content=full_html,
        output_epub_path=out_path
    )
    return out_path if success else None

def main():
    parser = argparse.ArgumentParser(description="中国网储系统性学习手册 EPUB 电子书构建工具")
    parser.add_argument("--module", type=str, help="指定构建单个板块 (如 L0, L1, SP4)")
    parser.add_argument("--full-only", action="store_true", help="仅构建全本合并 EPUB")
    args = parser.parse_args()

    toc_data = load_toc()
    combined_css = load_css()

    print(f"📖 触发 EPUB 构建流程，目标目录: {OUTPUT_DIR}")

    if args.module:
        target_code = args.module.upper()
        found_level = None
        for level in toc_data.get("levels", []):
            lid = level["id"]
            code = LEVEL_CODE_MAP.get(lid, lid.upper())
            if code == target_code or lid == target_code.lower():
                found_level = level
                break
        if found_level:
            build_single_module(found_level, combined_css)
        else:
            print(f"❌ 找不到对应板块: {args.module}")
            sys.exit(1)
        return

    if args.full_only:
        build_full_book(toc_data, combined_css)
        return

    # 默认构建所有可用板块 + 全本合并 EPUB
    built_files = []
    for level in toc_data.get("levels", []):
        ep = build_single_module(level, combined_css)
        if ep:
            built_files.append(ep)

    full_ep = build_full_book(toc_data, combined_css)
    if full_ep:
        built_files.append(full_ep)

    print("\n🎉 EPUB 电子书构建完成！文件列表：")
    for f in built_files:
        print(f"  • {f.name} ({f.stat().st_size / 1024:.1f} KB)")

if __name__ == "__main__":
    main()
