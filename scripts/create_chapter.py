#!/usr/bin/env python3
"""
网储系统性学习手册 — 新章节脚手架模板生成脚本
用法：
  python3 scripts/create_chapter.py <section_id>

示例：
  python3 scripts/create_chapter.py 01_2_1
"""

import sys
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TOC_PATH = ROOT_DIR / "data" / "toc.json"

def main():
    if len(sys.argv) < 2:
        print("错误: 请提供章节编号 (如 01_2_1)")
        sys.exit(1)

    section_id = sys.argv[1].strip()

    if not TOC_PATH.exists():
        print(f"错误: 找不到 {TOC_PATH}")
        sys.exit(1)

    with open(TOC_PATH, "r", encoding="utf-8") as f:
        toc = json.load(f)

    # 查找章节及相邻章节信息
    all_sections = []
    for level in toc.get("levels", []):
        level_id = level.get("id")
        level_name = level.get("title", "")
        for chapter in level.get("chapters", []):
            chapter_name = chapter.get("title", "")
            for sec in chapter.get("sections", []):
                all_sections.append({
                    "id": sec.get("id"),
                    "title": sec.get("title"),
                    "file": sec.get("file"),
                    "level_id": level_id,
                    "level_name": level_name,
                    "chapter_name": chapter_name
                })

    target_idx = None
    for idx, s in enumerate(all_sections):
        if s["id"] == section_id:
            target_idx = idx
            break

    if target_idx is None:
        print(f"❌ 错误: 未在 toc.json 中找到 ID={section_id}")
        sys.exit(1)

    curr = all_sections[target_idx]
    prev_sec = all_sections[target_idx - 1] if target_idx > 0 else None
    next_sec = all_sections[target_idx + 1] if target_idx < len(all_sections) - 1 else None

    target_dir = ROOT_DIR / "chapters" / curr["level_id"]
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / curr["file"]

    force_overwrite = "--force" in sys.argv
    if target_file.exists() and not force_overwrite:
        print(f"⚠️ 提示: 文件 {target_file.relative_to(ROOT_DIR)} 已存在，终止覆盖。如需强制滚回模板请附加 --force 参数。")
        sys.exit(0)

    # 生成 HTML 骨架
    prev_top_link = f'<a href="{prev_sec["file"]}" class="nav-prev" title="上一节：{prev_sec["title"]}">← 上节</a>' if prev_sec else '<a href="#" class="nav-prev disabled">← 上节</a>'
    next_top_link = f'<a href="{next_sec["file"]}" class="nav-next" title="下一节：{next_sec["title"]}">下节 →</a>' if next_sec else '<a href="#" class="nav-next disabled">下节 →</a>'

    prev_bottom_link = f'''<a href="{prev_sec["file"]}" class="bottom-nav-prev">
        <span class="bnav-label">← 上一节</span>
        <span class="bnav-title">{prev_sec["title"]}</span>
      </a>''' if prev_sec else '''<a href="#" class="bottom-nav-prev disabled">
        <span class="bnav-label">← 上一节</span>
        <span class="bnav-title">无（起始章节）</span>
      </a>'''

    next_bottom_link = f'''<a href="{next_sec["file"]}" class="bottom-nav-next">
        <span class="bnav-label">下一节 →</span>
        <span class="bnav-title">{next_sec["title"]}</span>
      </a>''' if next_sec else '''<a href="#" class="bottom-nav-next disabled">
        <span class="bnav-label">下一节 →</span>
        <span class="bnav-title">无（尾章节）</span>
      </a>'''

    html_template = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{curr["title"]} — {curr["chapter_name"]} | 网储学习手册</title>
  <meta name="description" content="本节深入剖析{curr["title"]}的核心物理原理、工程应用与实战案例。">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700&family=Inter:wght@400;500;700&family=JetBrains+Mono&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../assets/css/main.css">
  <script>
    window.MathJax = {{
      tex: {{
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
      }},
      options: {{
        skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
      }}
    }};
  </script>
  <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>

  <!-- ① 顶部固定导航栏 -->
  <nav class="top-nav" id="top-nav">
    <div class="top-nav-inner">
      <a href="../../index.html" class="nav-home" title="返回主页">
        <span class="nav-home-icon">⚡</span>
        <span class="nav-home-text">网储手册</span>
      </a>
      <div class="nav-breadcrumb">
        <span class="nav-level">{curr["level_id"].upper()}</span>
        <span class="nav-sep">›</span>
        <span class="nav-chapter">{curr["chapter_name"]}</span>
        <span class="nav-sep">›</span>
        <span class="nav-section">{curr["title"]}</span>
      </div>
      <div class="nav-chapter-jump">
        {prev_top_link}
        {next_top_link}
      </div>
    </div>
  </nav>

  <div class="page-wrapper">

    <!-- ② 章节页眉 -->
    <header class="chapter-header">
      <div class="breadcrumb">
        <span class="level-tag">{curr["level_id"].upper()}</span>
        <span class="sep">›</span>
        <span>{curr["chapter_name"]}</span>
        <span class="sep">›</span>
        <span>{curr["title"]}</span>
      </div>
      <div class="chapter-meta">
        <span class="file-id">{curr["id"]}</span>
        <span class="reading-time">⏱ 约25分钟</span>
        <span class="difficulty">🟢 入门</span>
      </div>
      <h1>{curr["title"]}</h1>
      <p class="chapter-lead">概括本节核心要点与现实应用价值。</p>
    </header>

    <!-- ③ 学习目标 -->
    <section class="learning-goals">
      <h2>📚 本节学习目标</h2>
      <ul>
        <li><strong>核心目标一</strong>：明确阐述该概念的基本含义与工程意义。</li>
        <li><strong>核心目标二</strong>：掌握主要数学公式与定量计算方法。</li>
        <li><strong>核心目标三</strong>：能结合实际网储工程案例分析与解决实际问题。</li>
      </ul>
    </section>

    <!-- ④ 场景引入 -->
    <section class="scene-intro">
      <h2>🔥 场景引入：[从具体工程问题/现实案例引入]</h2>
      <p>在这里撰写 200-400 字的场景引入或现实痛点描述……</p>
    </section>

    <!-- ⑤ 正文内容 -->
    <main class="chapter-content">
      <section>
        <h2>一、[主题一]</h2>
        <p>正文内容（目标 5,000+ 字）……</p>

        <div class="callout callout-analogy">
          <span class="callout-icon">🔍</span>
          <div class="callout-content">
            <strong>生活类比：[概念名称]</strong>
            <p>通过通俗易懂的生活场景类比解释该技术点……</p>
          </div>
        </div>
      </section>

      <section>
        <h2>二、[主题二]</h2>
        <p>正文内容……</p>

        <div class="callout callout-case">
          <span class="callout-icon">🏗️</span>
          <div class="callout-content">
            <strong>中国真实案例：[项目/政策名称]</strong>
            <p>详细分析国内真实网储电站应用或最新政策规章……</p>
          </div>
        </div>
      </section>
    </main>

    <!-- ⑥ 本节小结 -->
    <section class="chapter-summary">
      <h2>📝 本节小结</h2>
      <ul>
        <li><strong>要点一</strong>：精炼总结核心知识点。</li>
        <li><strong>要点二</strong>：概括主要计算结论或选型建议。</li>
        <li><strong>要点三</strong>：复盘工程注意事项。</li>
      </ul>
    </section>

    <!-- ⑦ 知识测验 -->
    <section class="quiz-section">
      <h2>❓ 知识测验</h2>

      <!-- Q1 -->
      <div class="quiz-question" id="q1">
        <p class="question-text"><strong>1.</strong> [题目一描述]</p>
        <div class="quiz-options">
          <label class="quiz-option"><input type="radio" name="q1" value="A"> A. 选项 A</label>
          <label class="quiz-option"><input type="radio" name="q1" value="B"> B. 选项 B</label>
          <label class="quiz-option"><input type="radio" name="q1" value="C"> C. 选项 C</label>
          <label class="quiz-option"><input type="radio" name="q1" value="D"> D. 选项 D</label>
        </div>
        <div class="quiz-answer" id="q1-answer" style="display:none">
          <p>✅ <strong>正确答案：A</strong></p>
          <p>📖 <strong>解析</strong>：100-150 字详细解析……</p>
        </div>
      </div>

      <button class="btn-check-answer" onclick="checkAnswers()">查看答案与解析</button>
      <p class="quiz-score" id="score-display"></p>
    </section>

    <!-- ⑧ 章节底部导航 -->
    <nav class="bottom-nav">
      {prev_bottom_link}
      <a href="../../index.html" class="bottom-nav-home">🏠 主页</a>
      {next_bottom_link}
    </nav>

    <!-- ⑨ 相关章节 -->
    <section class="cross-refs">
      <h2>🔗 相关章节</h2>
      <ul class="cross-ref-list">
        <li><a href="../../index.html">返回目录主页</a></li>
      </ul>
    </section>

    <!-- ⑩ 页脚 -->
    <footer class="chapter-footer">
      <p>中国网储系统性学习手册 v3.2 &nbsp;|&nbsp; <span class="file-id">{curr["id"]}</span></p>
    </footer>

  </div>

  <!-- 返回页首悬浮按钮 -->
  <button id="btnBackTop" class="btn-back-top" aria-label="返回页首" title="返回页首" onclick="window.scrollTo({{top:0,behavior:'smooth'}})"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 15l-6-6-6 6"/></svg></button>


  <script src="../../assets/js/quiz.js"></script>
</body>
</html>
'''

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(html_template)

    print(f"🎉 成功生成标准章节 HTML 骨架文件: {target_file.relative_to(ROOT_DIR)}")

if __name__ == "__main__":
    main()
