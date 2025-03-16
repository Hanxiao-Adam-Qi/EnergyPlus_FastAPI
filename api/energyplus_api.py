from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import sys
import json
from fastapi.responses import FileResponse
import mimetypes

# **确保 EnergyPlus 绑定的路径正确**
sys.path.append("/usr/local/EnergyPlus-24-1-0")
import uuid
from pyenergyplus.api import EnergyPlusAPI



# **创建 FastAPI 实例**
app = FastAPI(
    title="EnergyPlus API",
    version="1.0",
    description="Run EnergyPlus simulation and get results",
    servers=[  # ✅ 添加 servers 以确保 Dify 能正确解析
        {"url": "http://192.168.0.66:8000", "description": "Production server"}
    ]
)

# **EnergyPlus 相关路径（Docker 容器内部路径）**
BASE_DIR = "/app/data"
EXAMPLES_DIR = f"{BASE_DIR}/exampleFiles"
WEATHER_DIR = f"{BASE_DIR}/weatherData"
OUTPUT_DIR = f"{BASE_DIR}/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# **创建 EnergyPlus API 实例**
api = EnergyPlusAPI()

class SimulationRequest(BaseModel):
    idf_file: str  # IDF 文件名
    weather_file: str  # 天气数据文件名

# 运行 EnergyPlus 模拟
@app.post("/run-simulation", summary="Run EnergyPlus simulation", operation_id="run_simulation")
async def run_simulation(request: SimulationRequest):
    """ Run EnergyPlus simulation and return the result path """

    idf_path = os.path.join(EXAMPLES_DIR, request.idf_file)
    weather_path = os.path.join(WEATHER_DIR, request.weather_file)

    if not os.path.exists(idf_path):
        raise HTTPException(status_code=404, detail=f"IDF file not found: {idf_path}")
    if not os.path.exists(weather_path):
        raise HTTPException(status_code=404, detail=f"Weather file not found: {weather_path}")

    run_id = str(uuid.uuid4())
    run_output_dir = os.path.join(OUTPUT_DIR, run_id)
    os.makedirs(run_output_dir, exist_ok=True)

    state = api.state_manager.new_state()
    api.runtime.run_energyplus(state, [
        "-r", "-d", run_output_dir, "-w", weather_path, idf_path
    ])

    return {"message": "EnergyPlus simulation completed", "output_dir": run_output_dir, "run_id": run_id, "weather_file": weather_path, "idf_file": idf_path}

# 获取所有已完成的模拟结果列表
@app.get("/get-all-performed-simulation", summary="get all performed simulation", operation_id="get_all_results")
async def get_all_results():
    """ Get all the performed simulation """
    return {"results": os.listdir(OUTPUT_DIR)}

# 获取特定run_id的模拟结果下的所有结果文件的列表
@app.get("/get-simulation-result-file-list/{run_id}", summary="get all result files of a simulation", operation_id="get_all_results")
async def get_result_file_list(run_id: str):
    """ Get all the result files of a simulation """
    run_output_dir = os.path.join(OUTPUT_DIR, run_id)
    return {"results": os.listdir(run_output_dir)}

# 获取特定run_id下的特定结果文件
@app.get("/get-specific-result-file/{run_id}/{file_name}", summary="get a specific result file of a simulation", operation_id="get_specific_results")
async def get_specific_results(run_id: str, file_name: str):
    """ Get a specific result file of a simulation """
    run_output_dir = os.path.join(OUTPUT_DIR, run_id)
    if not os.path.exists(run_output_dir):
        raise HTTPException(status_code=404, detail="Invalid run ID or results not found")

    result_file = os.path.join(run_output_dir, file_name)
    if not os.path.exists(result_file):
        raise HTTPException(status_code=404, detail=f"Result file {file_name} not found")

    # 构建文件下载链接
    file_url = f"http://192.168.0.66:8000/download-result/{run_id}/{file_name}"
    return {
        "file_name": file_name,
        "download_url": file_url,
        "run_id": run_id
    }

# 下载特定run_id下的特定结果文件
@app.get("/download-result/{run_id}/{file_name}", summary="download result file", operation_id="download_result")
@app.head("/download-result/{run_id}/{file_name}", summary="get result file headers", operation_id="head_result")
async def download_result(run_id: str, file_name: str):
    """Download the actual file"""
    run_output_dir = os.path.join(OUTPUT_DIR, run_id)
    result_file = os.path.join(run_output_dir, file_name)

    if not os.path.exists(result_file):
        raise HTTPException(status_code=404, detail=f"Result file {file_name} not found")

    # 通过文件扩展名推断 MIME 类型
    mime_type, _ = mimetypes.guess_type(result_file)
    if mime_type is None:
        mime_type = "application/octet-stream"  # 默认值
    elif mime_type.startswith('text/'):
        mime_type = mime_type.split(';')[0]  # 确保不包含 `charset=utf-8`

    return FileResponse(
        path=result_file,
        media_type=mime_type,
        filename=file_name,
        headers={"Content-Type": mime_type}  # **强制设置去掉 `charset=utf-8`**
    )

# 获取所有示例文件列表
@app.get("/get-examples", summary="get examples of EnergyPlus simulation", operation_id="get_examples")
async def get_examples():
    """ Get the examples input files of EnergyPlus simulation """
    examples_list = os.listdir(EXAMPLES_DIR)
    return {"examples": examples_list}

# 获取所有天气文件列表
@app.get("/get-weathers", summary="get weathers of EnergyPlus simulation", operation_id="get_weathers")
async def get_weathers():
    """ Get the weather files of EnergyPlus simulation """
    weathers_list = os.listdir(WEATHER_DIR)
    return {"weathers": weathers_list}  # 直接返回 `list`
