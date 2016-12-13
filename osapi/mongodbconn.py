# _*_ coding:utf-8 _*_

import pymongo
from settings import DB_CONN


class MongoHelper(object):
    """mongodb连接类"""

    conn = None

    def __init__(self):
        self.conn = pymongo.MongoClient(DB_CONN)

    def getconn(self):
        return self.conn

    def close(self):
        self.conn.close()

