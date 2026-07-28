/**
 * quiz.js — 知识测验交互逻辑
 * 适用于全部 287 个章节 HTML
 */

// ── 测验逻辑 ───────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {

  // 绑定每道题的单题"查看答案"按钮（如存在）
  document.querySelectorAll('.quiz-question').forEach(function (q) {
    const qId = q.id;
    const btn = q.querySelector('.quiz-btn');
    const answer = q.querySelector('.quiz-answer');
    if (!btn || !answer) return;

    btn.addEventListener('click', function () {
      const selected = q.querySelector('input[type="radio"]:checked');
      if (!selected) {
        btn.textContent = '请先选择一个答案';
        setTimeout(() => { btn.textContent = '查看答案'; }, 1500);
        return;
      }
      answer.style.display = 'block';
      btn.style.display = 'none';
      
      // 高亮正确与选择的选项
      let correctValue = answer.dataset.correct;
      if (!correctValue) {
        const match = answer.textContent.match(/正确答案[：:]\s*([A-D])/i);
        if (match) correctValue = match[1].toUpperCase();
      }

      q.querySelectorAll('.quiz-option').forEach(function (opt) {
        opt.style.pointerEvents = 'none';
        opt.style.opacity = '0.7';
      });

      if (correctValue) {
        const correctOpt = q.querySelector('.quiz-option input[value="' + correctValue + '"]');
        if (correctOpt) {
          const optLabel = correctOpt.closest('.quiz-option');
          optLabel.style.opacity = '1';
          optLabel.style.background = '#D1FAE5';
          optLabel.style.borderColor = '#059669';
        }
      }
      
      // 记录进度
      markSectionProgress(window.location.pathname, qId);
    });
  });

  // 监听返回顶端按钮
  const btnTop = document.getElementById('btnBackTop');
  if (btnTop) {
    window.addEventListener('scroll', function () {
      btnTop.classList.toggle('visible', window.scrollY > 400);
    }, { passive: true });
  }

  // 阅读进度条（可选）
  const progressBar = document.getElementById('reading-progress');
  if (progressBar) {
    window.addEventListener('scroll', function () {
      const docH = document.documentElement.scrollHeight - window.innerHeight;
      const pct = docH > 0 ? (window.scrollY / docH) * 100 : 0;
      progressBar.style.width = Math.min(100, pct) + '%';
    }, { passive: true });
  }
});

// ── 全局检查答案函数 (适用于底部 <button onclick="checkAnswers()">) ────
function checkAnswers() {
  const questions = document.querySelectorAll('.quiz-question');
  if (!questions.length) return;

  let totalCount = questions.length;
  let correctCount = 0;
  let answeredCount = 0;

  questions.forEach(function (q) {
    const qId = q.id;
    const answerEl = q.querySelector('.quiz-answer');
    if (answerEl) {
      answerEl.style.display = 'block';
    }

    // 隐藏单题按键（如果存在）
    const singleBtn = q.querySelector('.quiz-btn');
    if (singleBtn) singleBtn.style.display = 'none';

    // 确定正确选项 (优先 data-correct，其次从解析中匹配 "正确答案：X")
    let correctValue = answerEl ? answerEl.dataset.correct : null;
    if (!correctValue && answerEl) {
      const match = answerEl.textContent.match(/正确答案[：:]\s*([A-D])/i);
      if (match) {
        correctValue = match[1].toUpperCase();
      }
    }

    const selectedInput = q.querySelector('input[type="radio"]:checked');
    if (selectedInput) {
      answeredCount++;
      if (correctValue && selectedInput.value.toUpperCase() === correctValue) {
        correctCount++;
      }
    }

    // 选项标记高亮
    q.querySelectorAll('.quiz-option').forEach(function (optLabel) {
      const input = optLabel.querySelector('input[type="radio"]');
      if (!input) return;

      const val = input.value.toUpperCase();
      if (val === correctValue) {
        optLabel.style.background = '#D1FAE5';
        optLabel.style.borderColor = '#059669';
        optLabel.style.fontWeight = 'bold';
        optLabel.style.opacity = '1';
      } else if (input.checked && val !== correctValue) {
        optLabel.style.background = '#FEE2E2';
        optLabel.style.borderColor = '#DC2626';
        optLabel.style.opacity = '0.9';
      }
    });

    markSectionProgress(window.location.pathname, qId);
  });

  // 显示总得分与结果展示
  const scoreEl = document.getElementById('score-display') || document.querySelector('.quiz-score');
  if (scoreEl) {
    scoreEl.style.display = 'block';

    if (answeredCount < totalCount) {
      scoreEl.innerHTML = '📊 您已作答 <strong>' + answeredCount + ' / ' + totalCount + '</strong> 题（答对 ' + correctCount + ' 题）。答案与详细解析已在上方显示。';
    } else {
      scoreEl.innerHTML = '🎉 测验完成！您的得分：<strong>' + correctCount + ' / ' + totalCount + '</strong>（正确率 ' + Math.round(correctCount / totalCount * 100) + '%）。详细解析已在上方显示。';
    }
  }

  markSectionComplete(window.location.pathname);
}

// 导出至全局 window 对象，确保 HTML 内联 onclick 可直接触发
window.checkAnswers = checkAnswers;

// ── 进度持久化（localStorage）────────────────────────────────────
function getProgress() {
  try {
    return JSON.parse(localStorage.getItem('bess_progress') || '{}');
  } catch (e) { return {}; }
}

function saveProgress(data) {
  try { localStorage.setItem('bess_progress', JSON.stringify(data)); } catch (e) {}
}

function markSectionProgress(path, questionId) {
  const data = getProgress();
  const key = path.split('/').pop().replace('.html', '');
  if (!data[key]) data[key] = { started: true, questions: [] };
  if (!data[key].questions.includes(questionId)) {
    data[key].questions.push(questionId);
  }
  saveProgress(data);
}

function markSectionComplete(path) {
  const data = getProgress();
  const key = path.split('/').pop().replace('.html', '');
  if (!data[key]) data[key] = {};
  data[key].completed = true;
  data[key].completedAt = new Date().toISOString();
  saveProgress(data);
  // 通知导览页刷新（如在 iframe 内）
  if (window.parent && window.parent !== window) {
    window.parent.postMessage({ type: 'section_complete', key: key }, '*');
  }
}

// 导出给章节页手动调用
window.BESSQuiz = { getProgress, markSectionComplete, checkAnswers };
