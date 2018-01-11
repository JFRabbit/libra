# coding: utf-8

import MySQLdb
from constant.baseConstant import *
from util.yamlUtil import *
from util.jsonFormat import *


class MySQLManager(object):
    """数据库操作类"""

    def __init__(self, connection_name: str):
        """初始化：
                1 加载配置文件
                2 连接数据库
                3 设置光标
        """
        try:
            config = load_yaml(DB_CONFIG_PATH)

            self.__connect = MySQLdb.connect(
                host=config[MYSQL][connection_name][HOST],
                port=config[MYSQL][connection_name][PORT],
                user=config[MYSQL][connection_name][USER],
                passwd=config[MYSQL][connection_name][PASSWD],
                db=config[MYSQL][connection_name][DB],
                charset=config[MYSQL][connection_name][CHARSET]
            )
        except Exception as e:
            self.__isClose = True
            raise e

        self.__cursor = self.__connect.cursor()
        self.__isClose = False

    def __del__(self):
        self.close()

    def close(self):
        """关闭数据库连接"""
        if self.__isClose is False:
            self.__connect.close()
            self.__isClose = True

    def execute(self, sql):
        """执行SQL"""
        self.__cursor.execute(sql)

    def find(self, sql, find_all=True):
        """查询：
            如果all = True 返回所有数据
            否则只返回第一条数据
        """
        self.execute(sql)
        if find_all:
            return self.__cursor.fetchall()
        return self.__cursor.fetchone()

    def change(self, sql):
        """更改：
            可适用于增、删、改
        """
        try:
            num = self.__cursor.execute(sql)
            self.__connect.commit()
            return num
        except Exception as e:
            print(e)
            self.__connect.rollback()
            return 0


def sql_result_2_dict(select_items: tuple, result_items: tuple):
    if len(select_items) is 0 or len(result_items) is 0:
        raise Exception("Data length is 0")

    if len(select_items) is not len(result_items[0]):
        raise Exception("Data length different")

    if len(result_items) is 1:
        obj = {}
        for j in select_items:
            obj[j] = result_items[0][select_items.index(j)]

        print(json_format(obj))
        return obj

    result = []
    for i in result_items:
        obj = {}
        for j in select_items:
            obj[j] = i[select_items.index(j)]

        result.append(obj)

    print(json_format(result))
    return result


if __name__ == '__main__':
    help(MySQLManager)
    manager = MySQLManager("local")

    sql_find = 'SELECT * FROM foo'
    print(manager.find(sql_find))
    print(manager.find(sql_find, False))

    sql_insert = "INSERT INTO foo(foo_name) VALUE('Tom')"
    print(manager.change(sql_insert))
    print(manager.find(sql_find))

    data = manager.find(sql_find)  # type: tuple
    effect_num = data[-1][0]

    sql_update = "update foo set foo_name = 'Marry' where foo_id = '%d'" % effect_num
    print(manager.change(sql_update))
    print(manager.find(sql_find))

    sql_delete = "delete from foo where foo_id = '%d'" % effect_num
    print(manager.change(sql_delete))
    print(manager.find(sql_find))

    manager.close()
