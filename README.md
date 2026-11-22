# 电商接口自动化测试框架

基于 **pytest + requests + Allure + PyMySQL** 的接口自动化测试框架，覆盖电商系统的用户、商品、购物车三个模块。

框架采用「接口封装层 + 用例层 + 数据层」分层设计，支持接口间参数关联、CSV 数据驱动、数据库结果校验和 Allure 报告。

配套被测系统：`flask-ecommerce-api`（Flask + MySQL 电商后端）。

## 技术栈

- Python 3.10+
- pytest
- requests
- Allure
- PyMySQL
- python-dotenv

## 项目结构

```text
ecommerce-api-automation/
├── api/                    # 接口封装层
│   ├── user.py             # 登录、注册
│   ├── goods.py            # 商品列表、详情、新增
│   └── cart.py             # 购物车增删改查
├── testcases/              # 测试用例层
│   ├── test_user.py
│   ├── test_goods.py
│   └── test_cart.py
├── conf/                   # 服务地址、数据库、日志配置
├── data/
│   ├── login_data.csv      # 数据驱动用例数据
│   └── global.json         # 接口关联全局变量（token、商品 id）
├── utils/
│   ├── dbtools.py          # MySQL 操作封装
│   └── index.py            # 全局变量、CSV 读取
├── conftest.py             # fixture：登录、数据库、数据清理
├── pytest.ini
├── requirements.txt
└── .env.example
```

## 快速开始

### 1. 启动被测系统

先按照 `flask-ecommerce-api` 的 README 启动后端，确认 `http://127.0.0.1:8081` 可访问，并已执行 `python seed.py`。

### 2. 安装依赖

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
copy .env.example .env
```

默认配置即可连接本机后端和 MySQL。若被测服务地址或数据库账号不同，修改 `.env`。

### 4. 运行用例

```bash
# 全部用例
pytest

# 只跑冒烟用例
pytest -m smoke

# 只跑购物车模块
pytest -m cart
```

## 用例覆盖

| 模块 | 用例 | 校验点 |
|---|---|---|
| 用户 | 登录成功 | 返回 token，uid/username 与数据库一致 |
| 用户 | 登录失败（数据驱动） | 错误密码、不存在用户返回 -1 |
| 用户 | 登录参数缺失 | 缺少 password 返回 -4 |
| 用户 | 注册成功 | 新用户写入数据库 |
| 用户 | 重复注册 | 返回用户名已存在 -10 |
| 商品 | 商品列表分页 | 返回数量、总数与数据库一致 |
| 商品 | 商品详情 | 详情 id 与请求一致 |
| 商品 | 商品不存在 | 返回 -9 |
| 商品 | 新增商品 | 商品写入数据库，用后清理 |
| 商品 | 分页参数非法 | page=0 返回 -4 |
| 购物车 | 加入购物车 | 返回 cid，数量与数据库一致 |
| 购物车 | 重复添加 | 同一商品数量累加 |
| 购物车 | 购物车列表 | 总数、商品 id 正确 |
| 购物车 | 修改数量 | 数据库数量同步更新 |
| 购物车 | 删除商品 | 数据库记录删除 |
| 购物车 | 未携带 token | 返回 -8 |
| 购物车 | 非法 token | 返回 -3 |
| 购物车 | 商品不存在 | 返回 -4 |

共计 20 条用例（含参数化展开）。

## 设计说明

- **接口封装层**：`api/` 下按业务模块封装 requests 请求，用例只关心参数和断言，不重复写 URL 和请求头。
- **接口关联**：登录后把 `token`、`uid` 写入 `data/global.json`，商品列表把 `goodsID` 写入全局变量，购物车用例直接读取，解决接口依赖问题。
- **数据库断言**：关键用例不只断言接口返回，还通过 `utils/dbtools.py` 查询 MySQL，校验数据真正落库。
- **数据驱动**：登录异常场景放在 `data/login_data.csv`，用 `pytest.mark.parametrize` 参数化。
- **用例隔离**：`cleanCart` fixture 在每个购物车用例前后清理当前用户数据，避免用例互相影响。
- **日志与报告**：每类接口的请求参数、响应结果写入 `logs/api_auto.log`，pytest 结果输出到 Allure。

## 测试报告

```bash
pytest
allure serve allure-results
```

如果本机没有 Allure 命令行，可先安装：

```bash
# Windows 可用 scoop
scoop install allure
# 或下载 allure-commandline 后把 bin 目录加入 PATH
```

## 注意事项

- 运行前必须启动 `flask-ecommerce-api` 并初始化数据。
- 数据库断言依赖 MySQL；MySQL 不可用时相关用例会自动跳过，接口本身仍可测试。
- `.env` 和 `data/global.json` 属于本地运行配置，不要提交真实密码。

## 可写进简历的亮点

- 基于 pytest + requests 搭建分层接口自动化框架，覆盖用户、商品、购物车 3 个模块 20+ 条用例。
- 封装统一请求层与日志记录，使用全局变量解决登录 token、商品 id 的接口依赖问题。
- 引入 CSV 数据驱动和 MySQL 数据库断言，不仅校验响应码，还校验数据落库结果。
- 使用 fixture 完成登录复用和数据清理，保证用例独立、可重复执行，并接入 Allure 报告。

## License

MIT
