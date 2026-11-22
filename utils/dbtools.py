import pymysql


class DBtools():
    '''
    查询一条/多条
    修改，添加，删除
    '''
    def __init__(self, dict1):
        self.connDict = dict1
        self.conn = None
        self.cur = None

    def connect(self):
        self.conn = pymysql.connect(**self.connDict)
        self.cur = self.conn.cursor()

    # 关闭连接
    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    # 查询一条/多条
    def query(self, sql, params=[], count=0):
        result = []
        try:
            self.connect()
            self.cur.execute(sql, params)
        except Exception as result:
            print("查询异常：", result)
            return []
        else:
            if count == 0:
                result = self.cur.fetchall()
            elif count == 1:
                result = self.cur.fetchone()
            else:
                result = self.cur.fetchmany(count)
        finally:
            self.close()
        return result

    def update(self, sql, params=[]):
        try:
            self.connect()
            row_count = self.cur.execute(sql, params)
        except Exception as err:
            print("数据库执行异常详情：", err)
            if hasattr(self, "conn") and self.conn:
                self.conn.rollback()
            return 0
        else:
            self.conn.commit()
            return row_count
        finally:
            self.close()


if __name__ == '__main__':
    db = DBtools({
        "host": "127.0.0.1",
        "port": 3306,
        "database": "flask_shop",
        "user": "root",
        "password": "root",
        "charset": "utf8mb4"
    })
    data = db.query('select * from goods', [])
    print(data)
