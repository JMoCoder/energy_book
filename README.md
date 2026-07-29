# 中国网储系统性学习手册 (energy_book)

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Version](https://img.shields.io/badge/Version-v3.5-green.svg)
![Build Status](https://img.shields.io/badge/Deploy-GitHub%20Pages-orange.svg)

> **从零基础到网储专家** —— 涵盖电能基础、电力系统、电力市场、电化学、储能设备、系统工程、商业投资与前沿技术 8 大模块 + 看懂电费单、网储投建全流程、电力市场化交易 3 大专题，全书共 **308 个独立章节**，正文约 **155 万字**。

---

## 📖 项目简介

《中国网储系统性学习手册》是一个全景式的电化学与新型储能系统知识库平台。项目采用极简轻量、零依赖的现代化前端技术架构（HTML5 + CSS3 + Standard ESJavaScript），结合高可读性的结构化 JSON 目录索引，支持单页导航、全量模糊搜索以及响应式阅读体验。

### 🌟 核心特色
- **系统性课程体系**：从 Level 0 至 Level 8 递进式设计，覆盖物理/化学原理到百兆瓦级电站投资决策全链路；另设 SP1（看懂电费单）、SP2（网储投建全流程）、SP3（电力市场化交易）三大专题。
- **开箱即用与离线友好**：支持双击 `index.html` 直接离线阅读，无前端编译构建负担。
- **现代化视觉与 UI/UX**：内置响应式布局、高亮卡片导航、搜索筛选与难度标记。

---

## 📁 目录结构与数据安排

为了保障系统拓展性与多人协作效率，本手册采用**数据与渲染分离**的目录组织结构：

```text
energy_book/
├── index.html                # 主导览与阅读器 portal（渲染与交互逻辑）
├── LICENSE                   # MIT 开源许可协议
├── README.md                 # 项目使用与部署文档
├── .gitignore                # Git 忽略文件配置
├── .github/
│   └── workflows/
│       └── deploy.yml        # GitHub Actions 自动化部署工作流
├── data/
│   └── toc.json              # 目录大纲与元数据索引（存储章节映射与完成状态）
├── chapters/                 # 章节正文目录 (按 Level 划分子目录)
│   ├── level_00/             # Level 0 写在前面
│   ├── level_01/             # Level 1 电能基础知识
│   ├── level_02/             # Level 2 电力系统
│   ├── level_03/             # Level 3 电力市场与政策
│   ├── level_04/             # Level 4 电化学基础
│   ├── level_05/             # Level 5 储能设备与技术
│   ├── level_06/             # Level 6 系统工程与运营
│   ├── level_07/             # Level 7 商业投资与项目评估
│   ├── level_08/             # Level 8 前沿技术与专家视野
│   ├── sp_01/                # TOPIC SP1 看懂电费单与负荷曲线
│   ├── sp_02/                # TOPIC SP2 网储投建全流程
│   └── sp_03/                # TOPIC SP3 电力市场化交易专题
├── assets/                   # 静态资源目录（图片、样式图解等）
└── documents/                # 原始资料与大纲文档
```

### 1. 数据规范 (`data/toc.json`)
`toc.json` 是整个手册的知识图谱数据核心，负责定义目录层级、章节关联及阅读状态。结构示例如下：

```json
{
  "meta": {
    "title": "中国网储系统性学习手册",
    "version": "v3.5",
    "lastUpdated": "2026-07-29",
    "totalSections": 308,
    "totalWords": 1550000
  },
  "levels": [
    {
      "id": "level_01",
      "code": "01",
      "label": "LEVEL 1",
      "title": "电能基础知识",
      "chapters": [
        {
          "no": 1,
          "title": "电的基本概念",
          "sections": [
            {
              "id": "01_1_1",
              "file": "01_1_1_电荷基础.html",
              "title": "电荷：万物皆有电",
              "difficulty": "🟢",
              "words": 5000,
              "status": "published"
            }
          ]
        }
      ]
    }
  ]
}
```

### 2. 章节文件安排规范 (`chapters/`)
- 放置路径：`chapters/{level_id}/{file_name}`
- 命名规则：`{Level编号}_{章节编号}_{小节编号}_{标题关键词}.html` (例如 `chapters/level_01/01_1_1_电荷基础.html`)。
- 状态更新：完成新小节撰写后，只需将 HTML 放入对应 `level_xx` 目录，并在 `toc.json` 中将对应 section 的 `status` 调整为 `"published"` 即可自动在首页解锁阅读链接。

---

## 🚀 快速上手与部署指南

### 1. 本地预览 (Local Experience)
由于项目为纯静态应用，无需安装 Node.js 或构建工具：
- **方式 A (直接打开)**：双击根目录下的 `index.html` 即可启动阅读器。
- **方式 B (静态服务器)**：使用标准 CLI 启动静态服务：
  ```bash
  # Python 静态服务
  python3 -m http.server 8000

  # 或使用 npx serve
  npx serve .
  ```
  在浏览器访问 `http://localhost:8000` 即可。

---

### 2. GitHub Pages 自动部署 (推荐)
本项目已配置 GitHub Actions (`.github/workflows/deploy.yml`)。
1. 将代码推送到 GitHub 仓库的 `main` 分支。
2. 打开 GitHub 仓库，进入 **Settings** -> **Pages**。
3. 在 **Source** 下选择 **GitHub Actions**。
4. 每次提交代码或打 Tag 之后，GitHub Actions 会自动构建并发布到 GitHub Pages 访问链接（如 `https://<your-username>.github.io/energy_book/`）。

---

### 3. Nginx 生产环境部署
如使用云服务器 Nginx 托管项目，请按如下配置部署：

```nginx
server {
    listen 80;
    server_name energy-book.yourdomain.com;

    root /var/www/energy_book;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # 针对入口文件和数据文件禁掉强缓存，确保用户始终同步最新内容
    location ~* \.(html|json)$ {
        add_header Cache-Control "no-cache, no-store, must-revalidate";
        add_header Pragma "no-cache";
        add_header Expires 0;
    }

    # 针对静态资源（图片/字体/CSS/JS）开启长期缓存
    location ~* \.(css|js|jpg|jpeg|gif|png|ico|cur|gz|svg|svgz|mp4|ogg|ogv|webm|htc|woff|woff2)$ {
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }
}
```

---

## 🔄 版本更新与同步策略 (Update & Sync Strategy)

为了解决“在版本或文件更新后，已访问过的用户因浏览器或 CDN 缓存导致无法同步看到最新章节”的问题，项目建立了以下**三重同步策略**：

### 1. HTTP 响应头控制 (No-Cache Policy)
入口网页 `index.html` 以及目录元数据 `data/toc.json` 决不能被强缓存：
- 部署服务器/CDN 务必将 `.html` 和 `.json` 资源的 `Cache-Control` 设置为 `no-cache, no-store, must-revalidate`。
- 浏览器每次打开都会发起 `304` 协商验证，确保文件一旦在服务器更新，客户端立刻获取最新 `toc.json` 和 HTML 章节。

### 2. 版本号 Cache-Busting 机制
在 `data/toc.json` 的 `meta.version` 以及 `index.html` 的数据引用中引入版本号或时间戳：
- 每次更新目录或大章节时，同步升级 `data/toc.json` 中的 `version` 字段（如 `v1.0.0` -> `v1.1.0`）及 `lastUpdated` 字段。
- 在页面引用资源处（例如引入 JS/CSS 或 `fetch` 请求数据时）挂载版本 Query 参数：
  ```javascript
  fetch('data/toc.json?v=' + metaVersion)
  ```
  这样可以确保即使存在中间层代理，也能强制撕脱旧缓存。

### 3. GitHub Actions CI/CD 自动同步
通过项目自带的 GitHub Actions 工作流，只要 `main` 分支发生提交或推送了新的版本 Tag，Action 便会自动运行并刷新 GitHub Pages 的线上版本，用户无需人工干预即可在数秒内访问到包含最新章节的在线版本。

---

## 🏷️ Git 版本控制与打版本号规范

本项目严格遵守 [语义化版本 2.0.0 (SemVer)](https://semver.org/lang/zh-CN/) 规范，版本号格式为 `vX.Y.Z`：
- **X (主版本号/Major)**：出现重大结构重构或破坏性更新（例如数据结构彻底变革）。
- **Y (次版本号/Minor)**：新增完成的 Level 模块或大量集中上线的章节（例如完成 Level 1 全章）。
- **Z (修订号/Patch)**：针对已有章节的内容修正、错别字修复或样式微调。

### 常用 Git 操作指南

#### 1. 建立项目 Git 版本库与提交
```bash
# 初始化 Git 仓库
git init

# 设置默认分支名称为 main
git branch -M main

# 添加所有变更到暂存区
git add .

# 提交本地代码
git commit -m "feat: initial release of energy_book v1.0.0"
```

#### 2. 打版本号 Tag (Release Tagging)
```bash
# 创建附注标签 (Annotated Tag)
git tag -a v1.0.0 -m "Release v1.0.0: 完成中国网储系统性学习手册导览与首发版本库架构"

# 查看所有标签
git tag -n
```

#### 3. 推送到远程 GitHub 仓库
```bash
# 关联远程 Git 仓库
git remote add origin https://github.com/JMoCoder/energy_book.git

# 推送代码及所有标签到 GitHub
git push -u origin main --tags
```

#### 4. 后续发布更新流程 (版本递增规范)
当您撰写或修正了新的章节后：
```bash
# 1. 提交修改
git add .
git commit -m "docs: 新增 Level 1 电荷基础章节正文"

# 2. 打新的次版本号/修订号 Tag
git tag -a v1.1.0 -m "Release v1.1.0: 上线 Level 1 全部章节"

# 3. 推送到远程，自动触发部署同步
git push origin main --tags
```

---

## 📜 开源协议 (License)

本项目基于 [MIT 协议](LICENSE) 开源。任何人均可自由学习、复制、修改、分发及商业化使用，但须保留原作者版权声明。

Copyright (c) 2026 [JMoCoder](https://github.com/JMoCoder).
