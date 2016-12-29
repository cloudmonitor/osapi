# _*_ coding:utf-8 _*_

import pymongo
from settings import FLOWDB_CONN


class MongoHelper(object):
    """mongodb连接类"""

    conn = None

    def __init__(self, db_url):
        self.conn = pymongo.MongoClient(db_url)

    def getconn(self):
        return self.conn

    def close(self):
        self.conn.close()

