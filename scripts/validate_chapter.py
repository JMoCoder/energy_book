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

    # 4. 质量建议与硬性组件检查
    if 'callout-analogy' not in content:
        errors.append("缺少生活类比组件 (callout callout-analogy)：按深入浅出写作规范，每节必须包含生活类比！")

    if 'callout-case' not in content and 'callout-tips' not in content and 'callout-warning' not in content:
        warnings.append("建议使用侧边栏组件 (callout-case / callout-tips / callout-warning) 增强视觉层次")

    # 5. 测验区质量校验（禁止纯计算题、检查解析字数）
    quiz_answers = re.findall(r'<div[^>]*class=["\'][^"\']*quiz-answer[^"\']*["\'][^>]*>(.*?)</div>', content, re.DOTALL)
    if quiz_answers:
        if len(quiz_answers) < 5:
            warnings.append(f"测验题数量较少 ({len(quiz_answers)} 题)，标准要求为 5 道单选题")
        for idx, ans_text in enumerate(quiz_answers, 1):
            clean_ans = re.sub(r'<[^>]+>', '', ans_text).strip()
            if len(clean_ans) < 40:
                warnings.append(f"第 {idx} 题测验解析字数偏少 ({len(clean_ans)} 字)，建议补充为什么其他选项是错误的深度解析(80-150字)")
    else:
        errors.append("测验区域缺少解析节点 <div class=\"quiz-answer\">")

    # 检查测验题目是否包含计算题敏感词
    quiz_section_match = re.search(r'<section\s+class=["\'].*?quiz-section.*?["\']>(.*?)</section>', content, re.DOTALL)
    if quiz_section_match:
        quiz_html = quiz_section_match.group(1)
        calc_keywords = ["计算", "求出", "等于多少", "数值为", "多少A", "多少V", "多少W", "多少kW", "公式计算"]
        found_calc = [kw for kw in calc_keywords if kw in quiz_html]
        if found_calc:
            warnings.append(f"测验题中疑似包含计算题敏感词 {found_calc}，规范规定测验题严禁出计算题，应考察概念理解与辨析")

    # 6. 正文纯中文汉字长度与 H2 标题序号连续性检测
    main_match = re.search(r'<main[^>]*class=["\'].*?chapter-content.*?["\'][^>]*>(.*?)</main>', content, re.DOTALL)
    if main_match:
        main_html = main_match.group(1)
        chinese_chars = re.findall(r'[\u4e00-\u9fa5]', main_html)
        chinese_count = len(chinese_chars)
        if chinese_count < 6000:
            errors.append(f"正文 <main class=\"chapter-content\"> 内的纯中文汉字数未达标 (仅 {chinese_count} 字)，要求正文讲深讲透不少于 6,000 纯汉字！")
        
        # 检查 H2 标题中文序号连续性 (一、二、三...)
        h2_titles = re.findall(r'<h2>\s*([一二三四五六七八九十]+)、', main_html)
        cn_nums = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
        expected_seq = cn_nums[:len(h2_titles)]
        if h2_titles and h2_titles != expected_seq:
            errors.append(f"正文 H2 标题中文序号出现不连续或乱序: 实际为 {h2_titles}，期望为 {expected_seq}，请检查文章结构大纲！")
    else:
        errors.append("缺少正文核心节点 <main class=\"chapter-content\">")

    # 检查是否存在未填充的占位符
    placeholders = ["XX_X_X", "TODO", "［待补充］", "[待补充]", "此处填写"]
    found_placeholders = [ph for ph in placeholders if ph in content]
    if found_placeholders:
        warnings.append(f"检测到未填充的占位符: {found_placeholders}")

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
