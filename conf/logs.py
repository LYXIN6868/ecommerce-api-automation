import os
import time


class Logs:
    def __init__(self, url):
        # 日志路径
        self.url = url
        os.makedirs(os.path.dirname(url) or '.', exist_ok=True)

    def _write(self, level, info):
        timestr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        with open(self.url, 'a', encoding='utf-8') as file:
            file.write(
                f'[{timestr}] {level}\n'
                f' 接口名称：{info["name"]};\n'
                f' 接口路径：{info["url"]};\n'
                f' 请求参数：{info["params"]};\n'
                f' 返回结果：{info["result"]};\n\n'
            )

    # info 等级
    def info(self, **info):
        self._write('INFO', info)

    # error 等级
    def error(self, **info):
        self._write('ERROR', info)

    # debug 等级
    def debug(self, **info):
        self._write('DEBUG', info)


if __name__ == '__main__':
    logs = Logs('../logs/logs.log')
    logs.info(**{
        "name": "登录接口",
        "url": "请求路径",
        "params": {"请求参数": '值'},
        "result": {"参数": "值"}
    })
