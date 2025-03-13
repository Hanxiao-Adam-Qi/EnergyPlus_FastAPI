# EnergyPlus FastAPI 服务

这是一个基于FastAPI框架开发的EnergyPlus模拟服务API，提供了运行EnergyPlus模拟和获取模拟结果的功能。

## 功能特性

- 运行EnergyPlus模拟
- 获取模拟结果
- 下载模拟输出文件
- 管理示例文件和天气数据
- Docker容器化部署支持

## API端点

### 1. 运行模拟
- **POST** `/run-simulation`
  - 运行EnergyPlus模拟
  - 需要提供IDF文件和天气数据文件

### 2. 获取模拟结果
- **GET** `/get-all-performed-simulation`
  - 获取所有已完成的模拟列表
- **GET** `/get-simulation-result-file-list/{run_id}`
  - 获取特定模拟的所有结果文件
- **GET** `/get-specific-result-file/{run_id}/{file_name}`
  - 获取特定结果文件的下载链接
- **GET** `/download-result/{run_id}/{file_name}`
  - 下载特定的结果文件

### 3. 文件管理
- **GET** `/get-examples`
  - 获取可用的示例文件列表
- **GET** `/get-weathers`
  - 获取可用的天气数据文件列表

## 安装说明

### 使用Docker（推荐）

1. 确保已安装Docker和Docker Compose
2. 在项目根目录运行：
```bash
docker-compose up -d
```

### 手动安装

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 安装EnergyPlus（版本24.1.0）

3. 运行服务：
```bash
uvicorn api.energyplus_api:app --host 0.0.0.0 --port 8000
```

## 目录结构

```
fastAPI_energyPlus/
├── api/
│   ├── energyplus_api.py    # 主API文件
│   ├── requirements.txt     # Python依赖
│   ├── Dockerfile          # Docker配置
│   └── docker-compose.yml  # Docker Compose配置
├── data/
│   ├── exampleFiles/       # EnergyPlus示例文件
│   ├── weatherData/        # 天气数据文件
│   └── output/             # 模拟输出目录
└── README.md
```

## 使用示例

1. 运行模拟：
```bash
curl -X POST "http://localhost:8000/run-simulation" \
     -H "Content-Type: application/json" \
     -d '{"idf_file": "example.idf", "weather_file": "weather.epw"}'
```

2. 获取模拟结果：
```bash
curl "http://localhost:8000/get-all-performed-simulation"
```

## 注意事项

- 确保EnergyPlus已正确安装并配置
- 模拟结果将保存在`data/output`目录下
- 每个模拟运行都会生成唯一的`run_id`
- 建议使用Docker部署以确保环境一致性

## 许可证

MIT License