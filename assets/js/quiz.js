/**
 * quiz.js — 知识测验交互逻辑
 * 适用于全部 287 个章节 HTML
 */

// ── 测验逻辑 ───────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {

  // 自动在顶部导航栏注入 GitHub 链接
  const navInner = document.querySelector('.top-nav-inner');
  if (navInner && !navInner.querySelector('.nav-github-link')) {
    const ghLink = document.createElement('a');
    ghLink.href = 'https://github.com/JMoCoder/energy_book';
    ghLink.target = '_blank';
    ghLink.rel = 'noopener noreferrer';
    ghLink.className = 'nav-github-link';
    ghLink.title = '前往 GitHub 仓库';
    ghLink.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg><span>GitHub</span>`;
    navInner.appendChild(ghLink);
  }

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
    const handleScroll = function () {
      const scrollTop = window.scrollY || window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0;
      btnTop.classList.toggle('visible', scrollTop > 300);
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();

    btnTop.addEventListener('click', function (e) {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
      if (document.documentElement) {
        document.documentElement.scrollTo({ top: 0, behavior: 'smooth' });
      }
    });
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

// ── 进度持久化与云端/本地双路同步 ─────────────────────────────────
function normalizeProgressKeys(data) {
  if (!data || typeof data !== 'object') return {};
  const normalized = {};
  for (const key in data) {
    let decodedKey = key;
    try {
      decodedKey = decodeURIComponent(key);
    } catch (e) {}
    if (!normalized[decodedKey]) {
      normalized[decodedKey] = data[key];
    } else {
      normalized[decodedKey] = {
        ...normalized[decodedKey],
        ...data[key],
        completed: normalized[decodedKey].completed || data[key].completed,
        questions: Array.from(new Set([
          ...(normalized[decodedKey].questions || []),
          ...(data[key].questions || [])
        ]))
      };
    }
  }
  return normalized;
}

function getLocalProgress() {
  try {
    const raw = JSON.parse(localStorage.getItem('bess_progress') || '{}');
    return normalizeProgressKeys(raw);
  } catch (e) { return {}; }
}

function setLocalProgress(data) {
  try { localStorage.setItem('bess_progress', JSON.stringify(data)); } catch (e) {}
}

// 优先：从容器服务端 API (/api/progress) 获取进度，降级：回退至 localStorage 浏览器缓存
async function fetchProgressServer() {
  const localData = getLocalProgress();
  try {
    const res = await fetch('/api/progress', { cache: 'no-cache' });
    if (res.ok) {
      const json = await res.json();
      if (json && json.success && json.progress) {
        const merged = normalizeProgressKeys({ ...localData, ...json.progress });
        setLocalProgress(merged);
        return merged;
      }
    }
  } catch (e) {
    // API 不可用或纯静态模式，降级回退本地缓存
  }
  return localData;
}

// 优先：向容器服务端 API (/api/progress) 推送进度，降级：同时保存至 localStorage 浏览器缓存
async function saveProgressSync(data) {
  const normalized = normalizeProgressKeys(data);
  setLocalProgress(normalized); // 确保本地瞬间保存响应
  try {
    await fetch('/api/progress', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(normalized)
    });
  } catch (e) {
    // API 不可用（如 file:// 或纯静态 Nginx），静默降级为 localStorage
  }
}

function markSectionProgress(path, questionId) {
  const data = getLocalProgress();
  const rawKey = path.split('/').pop().replace('.html', '');
  const key = decodeURIComponent(rawKey);
  if (!data[key]) data[key] = { started: true, questions: [] };
  if (!data[key].questions) data[key].questions = [];
  if (!data[key].questions.includes(questionId)) {
    data[key].questions.push(questionId);
  }
  saveProgressSync(data);
}

function markSectionComplete(path) {
  const data = getLocalProgress();
  const rawKey = path.split('/').pop().replace('.html', '');
  const key = decodeURIComponent(rawKey);
  if (!data[key]) data[key] = {};
  data[key].completed = true;
  data[key].completedAt = new Date().toISOString();
  saveProgressSync(data);

  // 通知导览页刷新（如在 iframe 内）
  if (window.parent && window.parent !== window) {
    window.parent.postMessage({ type: 'section_complete', key: key }, '*');
  }

  // 跨标签页/跨窗口广播通知
  try {
    if ('BroadcastChannel' in window) {
      const bc = new BroadcastChannel('bess_progress_channel');
      bc.postMessage({ type: 'section_complete', key: key });
      bc.close();
    }
  } catch (e) {}
}

// 导出至全局 window 对象
window.BESSQuiz = { 
  getProgress: getLocalProgress, 
  fetchProgressServer, 
  markSectionComplete, 
  checkAnswers 
};

