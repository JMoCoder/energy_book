/**
 * 中国网储系统性学习手册 · PWA 安装与设备兼容引擎
 * 支持：Windows 桌面端 / Linux 桌面端 / macOS / Android / iOS Safari
 */

(function () {
  'use strict';

  class PWAInstallEngine {
    constructor() {
      this.deferredPrompt = null;
      this.isStandalone = false;
      this.isIOS = false;
      this.isSafari = false;
      this.isDesktop = false;
      this.hasDismissedIOSPrompt = false;

      this.initEnvironment();
      this.initServiceWorker();
      this.initEventListeners();
      this.renderUIElements();
    }

    /**
     * 检测设备与运行环境
     */
    initEnvironment() {
      // 1. 判断是否已作为 Standalone 独立应用安装运行
      const isDisplayStandalone = window.matchMedia('(display-mode: standalone)').matches
        || window.matchMedia('(display-mode: window-controls-overlay)').matches;
      const isIOSStandalone = window.navigator.standalone === true;
      this.isStandalone = isDisplayStandalone || isIOSStandalone;

      // 2. 判断 OS & 浏览器类型
      const ua = navigator.userAgent || '';
      this.isIOS = /iPhone|iPad|iPod/i.test(ua) && !window.MSStream;
      this.isSafari = this.isIOS && /Safari/i.test(ua) && !/CriOS|FxiOS|EdgiOS/i.test(ua);
      this.isDesktop = !/Android|iPhone|iPad|iPod|Mobile|Tablet/i.test(ua);

      // 从 localStorage 获取用户是否主动关闭过提示
      this.hasDismissedIOSPrompt = localStorage.getItem('pwa_ios_prompt_dismissed') === 'true';
    }

    /**
     * 注册 Service Worker
     */
    initServiceWorker() {
      if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
          // 智能推断 SW 路径
          const swPath = this.getSwPath();
          navigator.serviceWorker.register(swPath)
            .then((registration) => {
              console.log('[PWA] ServiceWorker 注册成功:', registration.scope);
            })
            .catch((err) => {
              console.warn('[PWA] ServiceWorker 注册失败:', err);
            });
        });
      }
    }

    getSwPath() {
      const pathParts = window.location.pathname.split('/');
      // 若在 chapters 子目录下，需向上计算层级
      if (window.location.pathname.includes('/chapters/')) {
        const depth = pathParts.filter(p => p === 'chapters' || p.startsWith('level_')).length + 1;
        return '../'.repeat(depth) + 'sw.js';
      }
      return './sw.js';
    }

    /**
     * 绑定全局事件处理
     */
    initEventListeners() {
      // 1. 捕获浏览器原生 PWA 可安装事件 (Windows/Linux/Android/Chrome/Edge)
      window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        this.deferredPrompt = e;
        console.log('[PWA] 捕获到 beforeinstallprompt 事件');
        this.updateInstallButtonVisibility(true);
      });

      // 2. 捕获安装完成事件
      window.addEventListener('appinstalled', () => {
        this.deferredPrompt = null;
        this.isStandalone = true;
        this.updateInstallButtonVisibility(false);
        this.showToast('🎉 应用已成功安装至桌面/应用列表！', 'success');
      });

      // 3. 网络状态变化监听
      window.addEventListener('online', () => this.handleNetworkChange(true));
      window.addEventListener('offline', () => this.handleNetworkChange(false));
    }

    /**
     * 动态挂载 UI 节点 (安装按钮 & iOS 引导弹窗 & Toast 提示框)
     */
    renderUIElements() {
      // 插入 iOS 安装引导 Modal DOM
      if (!document.getElementById('pwa-ios-modal')) {
        const iosModalHTML = `
          <div id="pwa-ios-modal" class="pwa-modal-overlay" style="display:none;">
            <div class="pwa-modal-card">
              <div class="pwa-modal-header">
                <div class="pwa-modal-title">
                  <span class="pwa-icon-logo">⚡</span>
                  <h3>安装《网储手册》应用</h3>
                </div>
                <button id="pwa-ios-modal-close" class="pwa-modal-close-btn" aria-label="关闭">&times;</button>
              </div>
              <div class="pwa-modal-body">
                <p class="pwa-modal-subtitle">在 iOS 设备上轻松安装本应用，获得媲美原生 App 的全屏阅读体验：</p>
                <div class="pwa-ios-steps">
                  <div class="pwa-step-item">
                    <span class="pwa-step-num">1</span>
                    <span class="pwa-step-text">点击 Safari 底部导航栏的 <strong>分享图标</strong> <span class="pwa-inline-icon">⎕↑</span></span>
                  </div>
                  <div class="pwa-step-item">
                    <span class="pwa-step-num">2</span>
                    <span class="pwa-step-text">在弹出的菜单中向下滚动，选择 <strong>“添加到主屏幕”</strong> <span class="pwa-inline-icon">➕</span></span>
                  </div>
                  <div class="pwa-step-item">
                    <span class="pwa-step-num">3</span>
                    <span class="pwa-step-text">点击右上角 <strong>“添加”</strong>，即可从主屏幕一键启动！</span>
                  </div>
                </div>
              </div>
              <div class="pwa-modal-footer">
                <button id="pwa-ios-dismiss-btn" class="pwa-btn pwa-btn-secondary">不再提醒</button>
                <button id="pwa-ios-gotit-btn" class="pwa-btn pwa-btn-primary">我知道了</button>
              </div>
            </div>
          </div>
        `;
        document.body.insertAdjacentHTML('beforeend', iosModalHTML);

        // 绑定 Modal 交互事件
        document.getElementById('pwa-ios-modal-close')?.addEventListener('click', () => this.hideIOSModal());
        document.getElementById('pwa-ios-gotit-btn')?.addEventListener('click', () => this.hideIOSModal());
        document.getElementById('pwa-ios-dismiss-btn')?.addEventListener('click', () => {
          localStorage.setItem('pwa_ios_prompt_dismissed', 'true');
          this.hideIOSModal();
        });
        document.getElementById('pwa-ios-modal')?.addEventListener('click', (e) => {
          if (e.target.id === 'pwa-ios-modal') this.hideIOSModal();
        });
      }

      // 挂载网络 Toast
      if (!document.getElementById('pwa-toast-container')) {
        const toastHTML = `<div id="pwa-toast-container" class="pwa-toast-container"></div>`;
        document.body.insertAdjacentHTML('beforeend', toastHTML);
      }

      // 如果页面 header 含有 pwa-install-trigger 节点，绑定点击事件
      this.bindHeaderInstallButton();

      // 如果是 iOS Safari 且非 Standalone 且未关闭提示，适当延时显示引导
      if (this.isIOS && !this.isStandalone && !this.hasDismissedIOSPrompt) {
        setTimeout(() => {
          this.showInstallPrompt();
        }, 3000);
      }
    }

    /**
     * 绑定页面上的安装触发按钮 (如 Header 上的按钮)
     */
    bindHeaderInstallButton() {
      const installBtns = document.querySelectorAll('.pwa-install-btn, #header-pwa-install');
      installBtns.forEach(btn => {
        btn.addEventListener('click', () => this.showInstallPrompt());
      });

      // 初始化显示状态
      if (this.isStandalone) {
        this.updateInstallButtonVisibility(false);
      } else if (this.deferredPrompt || this.isIOS) {
        this.updateInstallButtonVisibility(true);
      }
    }

    /**
     * 控制安装按钮的显隐
     */
    updateInstallButtonVisibility(show) {
      const installBtns = document.querySelectorAll('.pwa-install-btn, #header-pwa-install');
      installBtns.forEach(btn => {
        if (this.isStandalone) {
          btn.style.display = 'none';
        } else if (show) {
          btn.style.display = 'inline-flex';
          btn.classList.add('pwa-btn-pulse');
        } else {
          // 如果桌面端暂未捕获 event，保持显示，点击时提示手动安装说明
          btn.style.display = 'inline-flex';
          btn.classList.remove('pwa-btn-pulse');
        }
      });
    }

    /**
     * 执行安装流程
     */
    async showInstallPrompt() {
      // 1. Standalone 模式下无需安装
      if (this.isStandalone) {
        this.showToast('应用已在桌面独立窗口中运行', 'info');
        return;
      }

      // 2. 支持 beforeinstallprompt (Windows Desktop / Linux Desktop / Android Chrome & Edge)
      if (this.deferredPrompt) {
        try {
          this.deferredPrompt.prompt();
          const { outcome } = await this.deferredPrompt.userChoice;
          console.log(`[PWA] 用户安装选择结果: ${outcome}`);
          if (outcome === 'accepted') {
            this.showToast('正在为您安装桌面应用...', 'info');
          }
          this.deferredPrompt = null;
          this.updateInstallButtonVisibility(false);
        } catch (err) {
          console.error('[PWA] 触发安装发生错误:', err);
        }
        return;
      }

      // 3. iOS Safari 浏览器
      if (this.isIOS) {
        this.showIOSModal();
        return;
      }

      // 4. 其他桌面/移动浏览器 fallback (如 Firefox / 桌面 Safari)
      const platformName = this.isDesktop ? '桌面端' : '移动端';
      this.showToast(`提示：您可以点击${platformName}浏览器地址栏右侧的“安装/➕”图标，或在菜单中选择“添加至桌面/应用列表”。`, 'info', 6000);
    }

    showIOSModal() {
      const modal = document.getElementById('pwa-ios-modal');
      if (modal) {
        modal.style.display = 'flex';
        setTimeout(() => modal.classList.add('pwa-modal-active'), 10);
      }
    }

    hideIOSModal() {
      const modal = document.getElementById('pwa-ios-modal');
      if (modal) {
        modal.classList.remove('pwa-modal-active');
        setTimeout(() => { modal.style.display = 'none'; }, 300);
      }
    }

    /**
     * 网络离线/在线 Toast 提醒
     */
    handleNetworkChange(isOnline) {
      if (isOnline) {
        this.showToast('🟢 网络连接已恢复，重新同步数据中', 'success');
      } else {
        this.showToast('⚡ 已切换至离线阅读模式，支持离线浏览已缓存章节', 'warning', 5000);
      }
    }

    /**
     * 轻量 Toast 提示组件
     */
    showToast(message, type = 'info', duration = 3500) {
      const container = document.getElementById('pwa-toast-container');
      if (!container) return;

      const toast = document.createElement('div');
      toast.className = `pwa-toast pwa-toast-${type}`;
      toast.innerHTML = `<span class="pwa-toast-text">${message}</span>`;
      container.appendChild(toast);

      setTimeout(() => toast.classList.add('pwa-toast-show'), 10);

      setTimeout(() => {
        toast.classList.remove('pwa-toast-show');
        setTimeout(() => toast.remove(), 300);
      }, duration);
    }
  }

  // 页面加载自动实例化引擎
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      window.pwaEngine = new PWAInstallEngine();
    });
  } else {
    window.pwaEngine = new PWAInstallEngine();
  }
})();
