import pytest

from api.user import login, register
from conf.index import ADMINPWD, ADMINUSER
from utils.index import readCsv


class TestUser:
    @pytest.mark.user
    @pytest.mark.smoke
    def test_01_login(self, db):
        data = login({'username': ADMINUSER, 'password': ADMINPWD})
        assert data['code'] == 1
        assert data['msg'] == '登录成功'
        assert data['data']['token']
        # 数据库校验：返回的 uid、username 与数据库一致
        dbData = db.query('select username from users where uid=%s', [data['data']['uid']], 1)
        assert dbData[0] == data['data']['username']

    @pytest.mark.user
    @pytest.mark.parametrize('row', readCsv('login_data.csv'))
    def test_02_login_data(self, row):
        data = login({'username': row['username'], 'password': row['password']})
        assert data['code'] == int(row['expectCode'])
        assert row['expectMsg'] in data['msg']

    @pytest.mark.user
    def test_03_login_params_error(self):
        # 只传 username，缺少 password，应返回参数非法
        data = login({'username': ADMINUSER})
        assert data['code'] == -4
        assert data['msg'] == '参数非法'

    @pytest.mark.user
    def test_04_register(self, db, uniqueUser):
        data = register(uniqueUser)
        assert data['code'] == 1
        assert data['msg'] == '注册成功'
        # 数据库校验：注册成功后用户表新增一条记录
        dbData = db.query('select count(*) from users where username=%s', [uniqueUser['username']], 1)
        assert dbData[0] == 1

    @pytest.mark.user
    def test_05_register_duplicate(self, uniqueUser):
        register(uniqueUser)
        data = register(uniqueUser)
        assert data['code'] == -10
        assert data['msg'] == '用户名已存在'
