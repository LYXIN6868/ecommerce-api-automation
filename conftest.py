import time

import pytest

from api.goods import goodsList
from api.user import login
from conf.index import ADMINPWD, ADMINUSER, SQLCONF
from utils.dbtools import DBtools
from utils.index import readGlobalValue


# 整个测试会话只登录一次，token 写入全局变量
@pytest.fixture(scope='session')
def loginData():
    data = login({'username': ADMINUSER, 'password': ADMINPWD})
    assert data and data['code'] == 1, '登录失败，请先启动 flask-ecommerce-api 并执行 seed.py'
    return data['data']


# 数据库连接，MySQL 不可用时自动跳过数据库断言
@pytest.fixture(scope='session')
def db():
    dbTools = DBtools(SQLCONF)
    if not dbTools.query('select 1'):
        pytest.skip('MySQL 不可用，跳过数据库校验')
    return dbTools


# 每个购物车用例前后清空当前用户的购物车，保证用例独立
@pytest.fixture()
def cleanCart(db, loginData):
    db.update('delete from cart where uid=%s', [loginData['uid']])
    yield
    db.update('delete from cart where uid=%s', [loginData['uid']])


# 生成一个唯一用户名，用例结束后清理
@pytest.fixture()
def uniqueUser(db):
    username = f"test_{int(time.time() * 1000)}"
    yield {'username': username, 'password': '123456'}
    db.update('delete from users where username=%s', [username])


# 提供一个可用的商品 id，供详情和购物车用例使用
@pytest.fixture()
def goodsId():
    gid = readGlobalValue('goodsID')
    if gid is None:
        data = goodsList({'page': 1, 'size': 1})
        gid = data['data'][0]['gid']
    return gid
