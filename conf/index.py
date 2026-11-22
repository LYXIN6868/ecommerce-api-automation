import os

from dotenv import load_dotenv

load_dotenv()

BASEURL = os.getenv("BASEURL", "http://127.0.0.1:8081")
TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
LOGPATH = os.getenv("LOG_PATH", "logs/api_auto.log")

ADMINUSER = os.getenv("ADMIN_USER", "admin")
ADMINPWD = os.getenv("ADMIN_PASSWORD", "123456")

SQLCONF = {
    "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "root"),
    "database": os.getenv("MYSQL_DATABASE", "flask_shop"),
    "charset": "utf8mb4"
}
