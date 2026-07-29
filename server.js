/**
 * 中国网储系统性学习手册 · 容器化轻量服务 & 进度同步 API
 * 说明：零依赖原生 Node.js 服务，支持静态资源服务、Gzip 压缩及 /api/progress 跨端进度同步与持久化
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');

const PORT = process.env.PORT || 8080;
const DATA_DIR = path.join(__dirname, 'data', 'user_data');
const PROGRESS_FILE = path.join(DATA_DIR, 'progress.json');

// 确保用户进度数据目录存在
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

// 静态文件 MIME 类型映射
const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.webmanifest': 'application/manifest+json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.woff2': 'font/woff2'
};

const server = http.createServer((req, res) => {
  const parsedUrl = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  const pathname = parsedUrl.pathname;

  // 跨域支持 (CORS)
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  // ── 1. 进度同步 API 端点 (/api/progress) ─────────────────────
  if (pathname === '/api/progress') {
    // 优先：获取服务端存储的进度
    if (req.method === 'GET') {
      fs.readFile(PROGRESS_FILE, 'utf8', (err, data) => {
        if (err) {
          res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
          res.end(JSON.stringify({ success: true, progress: {} }));
          return;
        }
        try {
          const json = JSON.parse(data);
          res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
          res.end(JSON.stringify({ success: true, progress: json }));
        } catch (e) {
          res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
          res.end(JSON.stringify({ success: true, progress: {} }));
        }
      });
      return;
    }

    // 优先：保存/合并客户端提交的进度
    if (req.method === 'POST') {
      let body = '';
      req.on('data', chunk => { body += chunk; });
      req.on('end', () => {
        try {
          const newProgress = JSON.parse(body || '{}');
          let existing = {};
          if (fs.existsSync(PROGRESS_FILE)) {
            try {
              existing = JSON.parse(fs.readFileSync(PROGRESS_FILE, 'utf8'));
            } catch (e) {}
          }
          // 双向合并逻辑：保留最新完成状态与已答题数据
          const merged = { ...existing, ...newProgress };
          for (const key in newProgress) {
            if (existing[key] && newProgress[key]) {
              merged[key] = {
                ...existing[key],
                ...newProgress[key],
                completed: existing[key].completed || newProgress[key].completed,
                questions: Array.from(new Set([
                  ...(existing[key].questions || []),
                  ...(newProgress[key].questions || [])
                ]))
              };
            }
          }

          fs.writeFileSync(PROGRESS_FILE, JSON.stringify(merged, null, 2), 'utf8');
          res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
          res.end(JSON.stringify({ success: true, progress: merged }));
        } catch (e) {
          res.writeHead(400, { 'Content-Type': 'application/json; charset=utf-8' });
          res.end(JSON.stringify({ success: false, error: 'Invalid JSON body' }));
        }
      });
      return;
    }
  }

  // ── 2. 静态资源服务 ──────────────────────────────────────────
  let filePath = path.join(__dirname, decodeURIComponent(pathname));
  if (pathname === '/' || pathname === '') {
    filePath = path.join(__dirname, 'index.html');
  }

  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end('<h1>404 Not Found</h1><p>页面或资源未找到。</p>');
      return;
    }

    const ext = path.extname(filePath).toLowerCase();
    let contentType = MIME_TYPES[ext] || 'application/octet-stream';
    if (path.basename(filePath) === 'manifest.json') {
      contentType = 'application/manifest+json; charset=utf-8';
    }

    const acceptEncoding = req.headers['accept-encoding'] || '';

    // 通用与 PWA 特定响应头设置
    const responseHeaders = {
      'Content-Type': contentType,
      'Cache-Control': 'no-cache'
    };

    // 为 SW 和 Manifest 文件设置零缓存与 Service-Worker-Allowed
    if (path.basename(filePath) === 'sw.js') {
      responseHeaders['Service-Worker-Allowed'] = '/';
      responseHeaders['Cache-Control'] = 'no-cache, no-store, must-revalidate';
    } else if (path.basename(filePath) === 'manifest.json') {
      responseHeaders['Cache-Control'] = 'no-cache, no-store, must-revalidate';
    }

    // Gzip 压缩文本与代码文件
    if (/\bgzip\b/.test(acceptEncoding) && (ext === '.html' || ext === '.css' || ext === '.js' || ext === '.json' || ext === '.svg' || ext === '.webmanifest')) {
      responseHeaders['Content-Encoding'] = 'gzip';
      res.writeHead(200, responseHeaders);
      const raw = fs.createReadStream(filePath);
      raw.pipe(zlib.createGzip()).pipe(res);
    } else {
      res.writeHead(200, responseHeaders);
      fs.createReadStream(filePath).pipe(res);
    }
  });
});

server.listen(PORT, () => {
  console.log(`⚡ 中国网储系统性学习手册已部署运行于端口 ${PORT}`);
  console.log(`🌐 主页访问: http://localhost:${PORT}`);
  console.log(`🔄 进度同步 API: http://localhost:${PORT}/api/progress`);
});
