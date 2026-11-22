import random

import requests

from conf.index import BASEURL, LOGPATH, TIMEOUT
from conf.logs import Logs
from utils.index import writeGlobalValue

logs = Logs(LOGPATH)

GOODSLISTPATH = '/goods/list'
GOODSDETAILPATH = '/goods/detail'
GOODSADDPATH = '/goods/add'


# 获取商品列表
def goodsList(params={}):
    try:
        res = requests.get(BASEURL + GOODSLISTPATH, params=params, timeout=TIMEOUT)
    except Exception as result:
        logs.error(**{
            "name": "商品列表接口",
            "url": BASEURL + GOODSLISTPATH,
            "params": params,
            "result": result
        })
        return None
    else:
        result = res.json()
        # 记录一个商品 id，供商品详情、购物车用例使用
        if result.get('code') == 1 and result.get('data'):
            writeGlobalValue('goodsID', random.choice(result['data'])['gid'])
        logs.info(**{
            "name": "商品列表接口",
            "url": BASEURL + GOODSLISTPATH,
            "params": params,
            "result": result
        })
        return result


# 获取商品详情
def goodsDetail(gid):
    try:
        res = requests.get(f"{BASEURL}{GOODSDETAILPATH}/{gid}", timeout=TIMEOUT)
    except Exception as result:
        logs.error(**{
            "name": "商品详情接口",
            "url": f"{BASEURL}{GOODSDETAILPATH}/{gid}",
            "params": {"gid": gid},
            "result": result
        })
        return None
    else:
        result = res.json()
        logs.info(**{
            "name": "商品详情接口",
            "url": f"{BASEURL}{GOODSDETAILPATH}/{gid}",
            "params": {"gid": gid},
            "result": result
        })
        return result


# 添加商品（演示接口）
def goodsAdd(params):
    try:
        res = requests.post(BASEURL + GOODSADDPATH, json=params, timeout=TIMEOUT)
    except Exception as result:
        logs.error(**{
            "name": "添加商品接口",
            "url": BASEURL + GOODSADDPATH,
            "params": params,
            "result": result
        })
        return None
    else:
        result = res.json()
        logs.info(**{
            "name": "添加商品接口",
            "url": BASEURL + GOODSADDPATH,
            "params": params,
            "result": result
        })
        return result
