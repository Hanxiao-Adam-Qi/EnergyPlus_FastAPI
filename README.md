# FastAPI Dify 服务

这是一个基于 FastAPI 框架开发的 Dify 服务 API，为Dify 插件提供后端支持。

## 功能特性

- 与 Dify 平台交互
- Docker 容器化部署支持

## 安装和运行

1. 克隆项目到本地。
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 运行服务：
   ```bash
   uvicorn api.fastAPI_dify:app --host 0.0.0.0 --port 8000
   ```

## Docker 部署

1. 构建 Docker 镜像：
   ```bash
   docker build -t fastapi-dify .
   ```
2. 运行 Docker 容器：
   ```bash
   docker run -d -p 8000:8000 fastapi-dify
   ```

## 贡献

欢迎贡献代码！请提交 Pull Request 或报告问题。