import requests

from conf.index import BASEURL, LOGPATH, TIMEOUT
from conf.logs import Logs
from utils.index import readGlobalValue

logs = Logs(LOGPATH)

CARTLISTPATH = '/cart/list'
CARTADDPATH = '/cart/add'
CARTUPDATEPATH = '/cart/update'
CARTDELETEPATH = '/cart/delete'


# 从全局变量里取 token，购物车接口都要带
def getHeaders():
    token = readGlobalValue('token')
    return {'token': token} if token else {}


# 获取购物车列表
def cartList(params={}):
    try:
        res = requests.get(BASEURL + CARTLISTPATH, params=params, headers=getHeaders(), timeout=TIMEOUT)
    except Exception as result:
        logs.error(**{
            "name": "购物车列表接口",
            "url": BASEURL + CARTLISTPATH,
            "params": params,
            "result": result
        })
        return None
    else:
        result = res.json()
        logs.info(**{
            "name": "购物车列表接口",
            "url": BASEURL + CARTLISTPATH,
            "params": params,
            "result": result
        })
        return result


# 添加商品到购物车
def cartAdd(params):
    try:
        res = requests.post(BASEURL + CARTADDPATH, json=params, headers=getHeaders(), timeout=TIMEOUT)
    except Exception as result:
        logs.error(**{
            "name": "添加购物车接口",
            "url": BASEURL + CARTADDPATH,
            "params": params,
            "result": result
        })
        return None
    else:
        result = res.json()
        logs.info(**{
            "name": "添加购物车接口",
            "url": BASEURL + CARTADDPATH,
            "params": params,
            "result": result
        })
        return result


# 修改购物车数量
def cartUpdate(params):
    try:
        res = requests.post(BASEURL + CARTUPDATEPATH, json=params, headers=getHeaders(), timeout=TIMEOUT)
    except Exception as result:
        logs.error(**{
            "name": "修改购物车接口",
            "url": BASEURL + CARTUPDATEPATH,
            "params": params,
            "result": result
        })
        return None
    else:
        result = res.json()
        logs.info(**{
            "name": "修改购物车接口",
            "url": BASEURL + CARTUPDATEPATH,
            "params": params,
            "result": result
        })
        return result


# 删除购物车商品
def cartDelete(params):
    try:
        res = requests.post(BASEURL + CARTDELETEPATH, json=params, headers=getHeaders(), timeout=TIMEOUT)
    except Exception as result:
        logs.error(**{
            "name": "删除购物车接口",
            "url": BASEURL + CARTDELETEPATH,
            "params": params,
            "result": result
        })
        return None
    else:
        result = res.json()
        logs.info(**{
            "name": "删除购物车接口",
            "url": BASEURL + CARTDELETEPATH,
            "params": params,
            "result": result
        })
        return result
