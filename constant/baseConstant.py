# coding: utf-8
import sys

DB_CONFIG_PATH = sys.path[0][0:sys.path[0].index("libra")] + "libra" + '/config/db.yaml'

MYSQL = 'mysql'
HOST = 'host'
PORT = 'port'
USER = 'user'
PASSWD = 'passwd'
DB = 'db'
CHARSET = 'charset'

MONGO = 'mongo'

if __name__ == "__main__":
    print(DB_CONFIG_PATH)
