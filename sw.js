/**
 * 中国网储系统性学习手册 · Service Worker
 * 功能：提供离线缓存、资源渐进更新与全平台 PWA 安装保障
 */

const CACHE_NAME = 'energy-storage-book-v3.6';

// 核心预缓存资源清单 (App Shell)
const STATIC_ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './assets/css/main.css',
  './assets/js/quiz.js',
  './assets/js/pwa-install.js',
  './assets/images/pwa-icon.svg',
  './assets/images/pwa-icon-192.png',
  './assets/images/pwa-icon-512.png',
  './data/toc.json'
];

// 1. Service Worker 安装 phase
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[ServiceWorker] 预缓存静态资源文件');
      return Promise.all(
        STATIC_ASSETS.map((asset) =>
          cache.add(asset).catch((err) => {
            console.warn('[ServiceWorker] 资源预缓存跳过:', asset, err);
          })
        )
      );
    }).then(() => {
      return self.skipWaiting();
    })
  );
});

// 2. Service Worker 激活 phase (清理过期缓存)
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('[ServiceWorker] 清除旧版本缓存:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      return self.clients.claim();
    })
  );
});

// 3. 动态 Fetch 请求拦截策略
self.addEventListener('fetch', (event) => {
  const request = event.request;
  const url = new URL(request.url);

  // 跳过非 GET 请求与 API 端点 (如 /api/progress 直连服务端)
  if (request.method !== 'GET' || url.pathname.startsWith('/api/')) {
    return;
  }

  // 策略 A: HTML 网页及章节内容 -> Network-First (网络优先，断网降级读取缓存)
  if (request.headers.get('accept')?.includes('text/html') || url.pathname.endsWith('.html')) {
    event.respondWith(
      fetch(request)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const responseToCache = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(request, responseToCache));
          }
          return networkResponse;
        })
        .catch(() => {
          // 断网时从缓存提供
          return caches.match(request).then((cachedResponse) => {
            if (cachedResponse) {
              return cachedResponse;
            }
            // 若该特定章节尚未缓存，重定向至首页离线状态
            return caches.match('./index.html');
          });
        })
    );
    return;
  }

  // 策略 B: 静态资源 (CSS, JS, 图片, 字体) -> Cache-First with Network Update (缓存优先)
  event.respondWith(
    caches.match(request).then((cachedResponse) => {
      if (cachedResponse) {
        // 后台静默发起网络请求更新缓存 (Stale-While-Revalidate)
        fetch(request).then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            caches.open(CACHE_NAME).then((cache) => cache.put(request, networkResponse));
          }
        }).catch(() => {/* 忽略后台静默获取失败 */});

        return cachedResponse;
      }

      // 未命中缓存，正常发起网络请求并缓存
      return fetch(request).then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, responseToCache));
        }
        return networkResponse;
      });
    })
  );
});
