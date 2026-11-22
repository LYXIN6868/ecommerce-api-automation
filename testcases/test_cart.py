import pytest
import requests

from api.cart import cartAdd, cartDelete, cartList, cartUpdate
from conf.index import BASEURL, TIMEOUT


class TestCart:
    @pytest.mark.cart
    @pytest.mark.smoke
    def test_01_addCart(self, cleanCart, goodsId, db, loginData):
        data = cartAdd({'gid': goodsId, 'count': 2})
        assert data['code'] == 1
        assert data['msg'] == '加入购物车成功'
        # 数据库校验：购物车数量与接口返回一致
        dbData = db.query('select count from cart where cid=%s and uid=%s', [data['data']['cid'], loginData['uid']], 1)
        assert dbData[0] == 2

    @pytest.mark.cart
    def test_02_addCartAgain(self, cleanCart, goodsId, loginData):
        # 同一商品重复添加，数量应累加
        cartAdd({'gid': goodsId, 'count': 2})
        data = cartAdd({'gid': goodsId, 'count': 3})
        assert data['code'] == 1
        assert data['data']['count'] == 5
        listData = cartList()
        assert listData['total'] == 1

    @pytest.mark.cart
    def test_03_cartList(self, cleanCart, goodsId, loginData):
        addData = cartAdd({'gid': goodsId, 'count': 2})
        data = cartList()
        assert data['code'] == 1
        assert data['total'] == 1
        assert data['data'][0]['cid'] == addData['data']['cid']
        assert data['data'][0]['goodsID'] == goodsId

    @pytest.mark.cart
    def test_04_cartUpdate(self, cleanCart, goodsId, db, loginData):
        cid = cartAdd({'gid': goodsId, 'count': 2})['data']['cid']
        data = cartUpdate({'cid': cid, 'count': 5})
        assert data['code'] == 1
        assert data['msg'] == '修改成功'
        # 数据库校验：修改后的数量
        dbData = db.query('select count from cart where cid=%s', [cid], 1)
        assert dbData[0] == 5

    @pytest.mark.cart
    def test_05_cartDelete(self, cleanCart, goodsId, db):
        cid = cartAdd({'gid': goodsId, 'count': 2})['data']['cid']
        data = cartDelete({'cid': cid})
        assert data['code'] == 1
        assert data['msg'] == '删除成功'
        # 数据库校验：数据已删除
        dbData = db.query('select count(*) from cart where cid=%s', [cid], 1)
        assert dbData[0] == 0

    @pytest.mark.cart
    def test_06_noToken(self, goodsId):
        res = requests.post(BASEURL + '/cart/add', json={'gid': goodsId, 'count': 1}, timeout=TIMEOUT)
        assert res.json()['code'] == -8
        assert res.json()['msg'] == '身份认证丢失，请重新登录'

    @pytest.mark.cart
    def test_07_invalidToken(self, goodsId):
        res = requests.post(
            BASEURL + '/cart/add',
            json={'gid': goodsId, 'count': 1},
            headers={'token': 'abc'},
            timeout=TIMEOUT
        )
        assert res.json()['code'] == -3
        assert res.json()['msg'] == '身份认证失效，请重新登录'

    @pytest.mark.cart
    def test_08_goodsNotExist(self, cleanCart, loginData):
        data = cartAdd({'gid': 999999, 'count': 1})
        assert data['code'] == -4
