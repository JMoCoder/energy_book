/**
 * quiz.js — 知识测验交互逻辑
 * 适用于全部 287 个章节 HTML
 */

// ── 测验逻辑 ───────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {

  // 绑定每道题的"查看答案"按钮
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
      // 高亮选项
      q.querySelectorAll('.quiz-option').forEach(function (opt) {
        opt.style.pointerEvents = 'none';
        opt.style.opacity = '0.7';
      });
      const correctOpt = q.querySelector('.quiz-option input[value="' +
        answer.dataset.correct + '"]');
      if (correctOpt) {
        correctOpt.closest('.quiz-option').style.opacity = '1';
        correctOpt.closest('.quiz-option').style.background = '#D1FAE5';
        correctOpt.closest('.quiz-option').style.borderColor = '#059669';
      }
      // 记录进度
      markSectionProgress(window.location.pathname, qId);
    });
  });

  // 全部回答完后显示总分
  const quizSection = document.querySelector('.quiz-section');
  if (quizSection) {
    const scoreEl = quizSection.querySelector('.quiz-score');
    if (scoreEl) {
      document.querySelectorAll('.quiz-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
          setTimeout(checkAllAnswered, 100);
        });
      });
    }
  }

  function checkAllAnswered() {
    const all = document.querySelectorAll('.quiz-question');
    const answered = document.querySelectorAll('.quiz-answer[style*="block"]');
    if (answered.length === all.length && all.length > 0) {
      const scoreEl = document.querySelector('.quiz-score');
      if (scoreEl) {
        scoreEl.style.display = 'block';
        scoreEl.textContent = '🎉 完成本节测验！共 ' + all.length + ' 题全部作答';
        markSectionComplete(window.location.pathname);
      }
    }
  }

  // ── 返回顶端按钮 ───────────────────────────────────────────────
  const btnTop = document.getElementById('btnBackTop');
  if (btnTop) {
    window.addEventListener('scroll', function () {
      btnTop.classList.toggle('visible', window.scrollY > 400);
    }, { passive: true });
  }

  // ── 阅读进度条（可选）──────────────────────────────────────────
  const progressBar = document.getElementById('reading-progress');
  if (progressBar) {
    window.addEventListener('scroll', function () {
      const docH = document.documentElement.scrollHeight - window.innerHeight;
      const pct = docH > 0 ? (window.scrollY / docH) * 100 : 0;
      progressBar.style.width = Math.min(100, pct) + '%';
    }, { passive: true });
  }
});

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

// 导出给章节页手动调用（可选）
window.BESSQuiz = { getProgress, markSectionComplete };
