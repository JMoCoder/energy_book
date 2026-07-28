#!/usr/bin/env python3
"""
网储系统性学习手册 — 章节 HTML 结构与质量自动化校验脚本
用法：
  python3 scripts/validate_chapter.py <html_filepath_or_section_id>

示例：
  python3 scripts/validate_chapter.py chapters/level_00/00_1_2_手册使用指南.html
  python3 scripts/validate_chapter.py 00_1_2
"""

import sys
import re
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TOC_PATH = ROOT_DIR / "data" / "toc.json"

def validate_html_file(file_path: Path) -> tuple[list[str], list[str]]:
    """校验单 HTML 文件的结构合规性，返回 (errors, warnings)"""
    errors = []
    warnings = []

    if not file_path.exists():
        return [f"文件不存在: {file_path}"], []

    content = file_path.read_text(encoding="utf-8")

    # 1. 检查资源引用路径
    if 'href="../../assets/css/main.css"' not in content and 'href="../assets/css/main.css"' not in content:
        errors.append("未包含正确的 CSS 引用 ('../../assets/css/main.css')")
    
    if 'src="../../assets/js/quiz.js"' not in content and 'src="../assets/js/quiz.js"' not in content:
        errors.append("未包含正确的 Quiz JS 引用 ('../../assets/js/quiz.js')")

    # 2. 检查必需的关键 class 类名与元素
    has_quiz_tag = bool(re.search(r'<section\s+class=["\'].*?(quiz-section|chapter-quiz).*?["\']>', content))
    if not has_quiz_tag:
        errors.append("缺少测验区域节点 <section class=\"quiz-section\">")
    elif 'class="chapter-quiz"' in content and 'class="quiz-section"' not in content:
        warnings.append("测验区域建议统一使用 class=\"quiz-section\" 而非 \"chapter-quiz\"")

    if 'onclick="checkAnswers()"' not in content:
        errors.append("测验区域缺少提交答案按钮 <button ... onclick=\"checkAnswers()\">")

    if 'id="score-display"' not in content:
        errors.append("测验区域缺少得分展示节点 <p id=\"score-display\">")

    has_cross_tag = bool(re.search(r'<section\s+class=["\'].*?(cross-refs|related-chapters).*?["\']>', content))
    if not has_cross_tag:
        errors.append("缺少相关章节节点 <section class=\"cross-refs\">")
    elif 'class="related-chapters"' in content and 'class="cross-refs"' not in content:
        warnings.append("相关章节建议统一使用 class=\"cross-refs\" 而非 \"related-chapters\"")

    if 'class="cross-ref-list"' not in content:
        warnings.append("相关章节的 <ul> 建议添加 class=\"cross-ref-list\" 样式类名")

    if '<nav class="bottom-nav">' not in content:
        errors.append("缺少章节底部导航 <nav class=\"bottom-nav\">")

    if 'class="chapter-footer"' not in content and 'class="site-footer"' not in content:
        errors.append("缺少章节页脚节点 <footer class=\"chapter-footer\">")

    # 3. 检查 DOM 结构顺序：<section class="quiz-section"> 应该在 <nav class="bottom-nav"> 之前，<section class="cross-refs"> 应该在 <nav class="bottom-nav"> 之后
    match_quiz = re.search(r'<section\s+class=["\'].*?(quiz-section|chapter-quiz).*?["\']>', content)
    match_bnav = re.search(r'<nav\s+class=["\']bottom-nav["\']>', content)
    match_cross = re.search(r'<section\s+class=["\'].*?(cross-refs|related-chapters).*?["\']>', content)

    if match_quiz and match_bnav and match_quiz.start() > match_bnav.start():
        errors.append("DOM 顺序错误：知识测验 (<section class=\"quiz-section\">) 必须在 底部导航 (<nav class=\"bottom-nav\">) 之前")

    if match_cross and match_bnav and match_cross.start() < match_bnav.start():
        errors.append("DOM 顺序错误：相关章节 (<section class=\"cross-refs\">) 必须在 底部导航 (<nav class=\"bottom-nav\">) 之后")

    # 4. 质量建议检查
    if 'callout-analogy' not in content:
        warnings.append("建议至少包含一个生活类比组件 (callout-analogy)")

    if 'callout-case' not in content and 'callout-tips' not in content and 'callout-warning' not in content:
        warnings.append("建议使用侧边栏组件 (callout-case / callout-tips / callout-warning) 增强视觉层次")

    # 5. 正文长度大致估算
    clean_text = re.sub(r'<[^>]+>', '', content)
    char_count = len(clean_text)
    if char_count < 3000:
        warnings.append(f"章节文字总量偏少 ({char_count} 字)，建议丰富正文内容至 5000+ 字")

    return errors, warnings

def resolve_file(arg: str) -> Path:
    p = Path(arg)
    if p.exists() and p.is_file():
        return p

    # 尝试作为 section_id 解析
    sec_id = arg.strip()
    if TOC_PATH.exists():
        with open(TOC_PATH, 'r', encoding='utf-8') as f:
            toc = json.load(f)
        for level in toc.get("levels", []):
            for chapter in level.get("chapters", []):
                for sec in chapter.get("sections", []):
                    if sec.get("id") == sec_id:
                        return ROOT_DIR / "chapters" / level.get("id") / sec.get("file")
    
    # 全局查找匹配文件名
    found = list(ROOT_DIR.glob(f"chapters/**/{sec_id}*.html"))
    if found:
        return found[0]

    return p

def main():
    if len(sys.argv) < 2:
        print("用法: python3 scripts/validate_chapter.py <html_filepath_or_section_id>")
        sys.exit(1)

    target_path = resolve_file(sys.argv[1])
    print(f"🔍 正在校验文件: {target_path.relative_to(ROOT_DIR) if target_path.is_relative_to(ROOT_DIR) else target_path}")
    
    errors, warnings = validate_html_file(target_path)

    if warnings:
        print("\n⚠️ 质量改进建议 (Warnings):")
        for w in warnings:
            print(f"  • {w}")

    if errors:
        print("\n❌ 发现严重错误 (Errors):")
        for e in errors:
            print(f"  • {e}")
        print("\n🚫 校验未通过，请修正上述错误后再发布。")
        sys.exit(1)
    else:
        print("\n✅ 所有规范校验通过！结构完备，无缺漏。")
        sys.exit(0)

if __name__ == "__main__":
    main()
