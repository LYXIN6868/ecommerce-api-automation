# 封装公共操作函数
import csv
import json
import os

# 项目根目录/data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATA_FILE = os.path.join(DATA_DIR, 'global.json')


# 写入全局变量，用于接口间参数关联
def writeGlobalValue(key, value):
    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        result = json.loads(file.read() or '{}')
    result[key] = value
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        file.write(json.dumps(result, ensure_ascii=False, indent=4))


# 读取全局变量
def readGlobalValue(key):
    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        result = json.loads(file.read() or '{}')
    return result.get(key)


# 读取 CSV 测试数据
def readCsv(filename):
    with open(os.path.join(DATA_DIR, filename), 'r', encoding='utf-8-sig') as file:
        return list(csv.DictReader(file))
