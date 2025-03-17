# 选择 Python 3.12 作为基础镜像
FROM python:3.12

# 设置工作目录
WORKDIR /app

# 安装 Node.js 和 npm
RUN apt-get update && apt-get install -y curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# 安装 Turndown.js 和 joplin-turndown-plugin-gfm
RUN npm install turndown joplin-turndown-plugin-gfm

# 复制 `requirements.txt` 并安装依赖（利用缓存）
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码（本地开发时会挂载，所以这一行不会生效）
COPY . /app

# 设置 PYTHONPATH，让 Python 能找到 EnergyPlus
ENV PYTHONPATH="/usr/local/EnergyPlus-24-1-0:$PYTHONPATH"

# 开启 FastAPI 开发模式（自动重载）
CMD ["uvicorn", "fastAPI_dify:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
