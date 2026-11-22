import time

import pytest

from api.goods import goodsAdd, goodsDetail, goodsList


class TestGoods:
    @pytest.mark.goods
    @pytest.mark.smoke
    def test_01_goodsList(self, db):
        data = goodsList({'page': 1, 'size': 5})
        assert data['code'] == 1
        assert len(data['data']) == 5
        assert data['data'][0]['goodsname']
        assert data['data'][0]['goodsprice'] > 0
        # 数据库校验：分页总数与数据库商品总数一致
        dbCount = db.query('select count(*) from goods', [], 1)[0]
        assert data['total'] == dbCount

    @pytest.mark.goods
    def test_02_goodsDetail(self, goodsId):
        data = goodsDetail(goodsId)
        assert data['code'] == 1
        assert data['data']['gid'] == goodsId
        assert data['data']['goodsname']

    @pytest.mark.goods
    def test_03_goodsDetailNotExist(self):
        data = goodsDetail(999999)
        assert data['code'] == -9
        assert data['msg'] == '数据或接口不存在'

    @pytest.mark.goods
    def test_04_goodsAdd(self, db):
        goodsName = f'测试商品_{int(time.time() * 1000)}'
        try:
            data = goodsAdd({'goodsname': goodsName, 'goodsprice': 99.9})
            assert data['code'] == 1
            assert data['msg'] == '添加商品成功'
            # 数据库校验：商品确实写入数据库
            dbData = db.query('select gid from goods where goodsname=%s', [goodsName], 1)
            assert dbData
        finally:
            db.update('delete from goods where goodsname=%s', [goodsName])

    @pytest.mark.goods
    def test_05_goodsListParamsError(self):
        # page 必须大于 0
        data = goodsList({'page': 0, 'size': 5})
        assert data['code'] == -4
