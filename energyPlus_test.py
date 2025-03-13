import os
import sys
sys.path.append("/usr/local/EnergyPlus-24-1-0")
from pyenergyplus.api import EnergyPlusAPI

# 创建 EnergyPlus API 实例
api = EnergyPlusAPI()

# 设定 EnergyPlus 输入文件路径（请修改为你的实际路径）
idf_path = "/home/adam/energyPlus/data/exampleFiles/1ZoneDataCenterCRAC_wApproachTemp.idf"  # 示例 IDF 文件
weather_path = "/home/adam/energyPlus/data/weatherData/USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw"  # 示例天气文件

# 确保 IDF 和天气文件存在
if not os.path.exists(idf_path):
    raise FileNotFoundError(f"IDF 文件不存在: {idf_path}")

if not os.path.exists(weather_path):
    raise FileNotFoundError(f"天气文件不存在: {weather_path}")

# 运行 EnergyPlus 模拟
state = api.state_manager.new_state()
api.runtime.run_energyplus(state, [
    "-r",           # 运行模拟并生成报告
    "-d", "/home/adam/energyPlus/output", # 输出目录
    "-w", weather_path, # 天气数据文件
    idf_path  # IDF 模型文件
])

print("EnergyPlus 模拟完成！请查看 output 目录中的结果文件。")
