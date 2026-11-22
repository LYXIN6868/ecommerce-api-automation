import requests

from conf.index import BASEURL, LOGPATH, TIMEOUT
from conf.logs import Logs
from utils.index import writeGlobalValue

logs = Logs(LOGPATH)

LOGINPATH = "/account/login"
REGISTPATH = "/account/register"


# 登录接口
def login(params):
    try:
        res = requests.post(BASEURL + LOGINPATH, json=params, timeout=TIMEOUT)
    except Exception as result:
        logs.error(**{
            "name": "登录接口",
            "url": BASEURL + LOGINPATH,
            "params": params,
            "result": result
        })
        return None
    else:
        result = res.json()
        # 登录成功后把 token 和 uid 写入全局变量，供购物车接口使用
        if result.get('code') == 1 and result.get('data'):
            writeGlobalValue('token', result['data']['token'])
            writeGlobalValue('uid', result['data']['uid'])
        logs.info(**{
            "name": "登录接口",
            "url": BASEURL + LOGINPATH,
            "params": params,
            "result": result
        })
        return result


# 注册接口
def register(params):
    try:
        res = requests.post(BASEURL + REGISTPATH, json=params, timeout=TIMEOUT)
    except Exception as result:
        logs.error(**{
            "name": "注册接口",
            "url": BASEURL + REGISTPATH,
            "params": params,
            "result": result
        })
        return None
    else:
        result = res.json()
        logs.info(**{
            "name": "注册接口",
            "url": BASEURL + REGISTPATH,
            "params": params,
            "result": result
        })
        return result
