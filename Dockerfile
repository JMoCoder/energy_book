# ── 中国网储系统性学习手册 容器化 Dockerfile ────────────────────────
FROM node:20-alpine

# 设置工作目录
WORKDIR /app

# 复制项目全量文件
COPY . .

# 创建持久化用户数据目录
RUN mkdir -p /app/data/user_data

# 暴露服务端口
EXPOSE 8080

# 环境变量
ENV PORT=8080

# 启动原生 Node.js 服务
CMD ["node", "server.js"]
