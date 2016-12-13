# _*_ coding:utf-8 _*_

from __future__ import division
import time
import pymongo

from mongodbconn import MongoHelper


def get_tenant_top_src_ip(tenant_id):
    conn = MongoHelper().getconn()
    db = conn["flowdb"]
    result = db.flow.aggregate([{"$match": {"project_id": "fab30037b2d54be484520cd16722f63c",
                                            "timestap": {"$gte": int(time.time() * 1000) - 10 * 60 * 1000}}},
                                {"$group": {"_id": "$ipsource", "count": {"$sum": 1}}},
                                {"$sort": {"count": -1}},
                                {"$limit": 10}])
    print list(result)
    conn.close()


def get_tenant_top_dst_ip(tenant_id):
    conn = MongoHelper().getconn()
    db = conn["flowdb"]
    result = db.flow.aggregate([{"$match": {"project_id": "fab30037b2d54be484520cd16722f63c",
                                            "timestap": {"$gte": int(time.time() * 1000)-10*60*1000}}},
                                {"$group": {"_id": "$ipdestination", "count": {"$sum": 1}}},
                                {"$sort": {"count": -1}},
                                {"$limit": 10}])
    print list(result)
    conn.close()


def get_instance_top_src_ip(tenant_id, instance_id):
    conn = MongoHelper().getconn()
    db = conn["flowdb"]
    result = db.flow.aggregate([{"$match": {"project_id": "fab30037b2d54be484520cd16722f63c",
                                            "instance_id": "b18ff7c9-70cc-4781-ad31-af9845e005db",
                                            "timestap": {"$gte": int(time.time() * 1000)-10*60*1000}}},
                                {"$group": {"_id": "$ipsource", "count": {"$sum": 1}}},
                                {"$sort": {"count": -1}},
                                {"$limit": 10}])
    print list(result)
    conn.close()


def get_instance_top_dst_ip(tenant_id, instance_id):
    conn = MongoHelper().getconn()
    db = conn["flowdb"]
    result = db.flow.aggregate([{"$match": {"project_id": "fab30037b2d54be484520cd16722f63c",
                                            "instance_id": "b18ff7c9-70cc-4781-ad31-af9845e005db",
                                            "timestap": {"$gte": int(time.time() * 1000)-10*60*1000}}},
                                {"$group": {"_id": "$ipdestination", "count": {"$sum": 1}}},
                                {"$sort": {"count": -1}},
                                {"$limit": 10}])
    print list(result)
    conn.close()


def get_instance_top_src_port(tenant_id, instance_id):
    conn = MongoHelper().getconn()
    db = conn["flowdb"]
    result = db.flow.aggregate([{"$match": {"project_id": "fab30037b2d54be484520cd16722f63c",
                                            "instance_id": "b18ff7c9-70cc-4781-ad31-af9845e005db",
                                            "timestap": {"$gte": int(time.time() * 1000)-10*60*1000},
                                            "ipprotocol": {"$in": [6, 17]}}},
                                {"$group": {"_id": "$srcport_or_icmptype", "count": {"$sum": 1}}},
                                {"$sort": {"count": -1}},
                                {"$limit": 10}])
    print list(result)
    conn.close()


def get_instance_top_dst_port(tenant_id, instance_id):
    conn = MongoHelper().getconn()
    db = conn["flowdb"]
    result = db.flow.aggregate([{"$match": {"project_id": "fab30037b2d54be484520cd16722f63c",
                                            "instance_id": "b18ff7c9-70cc-4781-ad31-af9845e005db",
                                            "timestap": {"$gte": int(time.time() * 1000)-10*60*1000},
                                            "ipprotocol": {"$in": [6, 17]}}},
                                {"$group": {"_id": "$dstport_or_icmpcode", "count": {"$sum": 1}}},
                                {"$sort": {"count": -1}},
                                {"$limit": 10}])
    print list(result)
    conn.close()


def get_tenant_top_instance(tenant_id):
    conn = MongoHelper().getconn()
    db = conn["flowdb"]
    result = db.flow.aggregate([{"$match": {"project_id": "fab30037b2d54be484520cd16722f63c",
                                            "timestap": {"$gte": int(time.time() * 1000) - 10 * 60 * 1000}}},
                                {"$group": {"_id": "$instance_id", "count": {"$sum": "$size"}}},
                                {"$sort": {"count": -1}},
                                {"$limit": 10}])
    print list(result)
    conn.close()


def get_instance_tcpflags_syn_flood(tenant_id, instance_id):
    conn = MongoHelper().getconn()
    db = conn["flowdb"]
    result = db.flow.aggregate([{"$match": {"project_id": "fab30037b2d54be484520cd16722f63c",
                                            "instance_id": "b18ff7c9-70cc-4781-ad31-af9845e005db",
                                            "timestap": {"$gte": int(time.time() * 1000)-10*60*1000},
                                            "ipprotocol": 6,
                                            "tcpflags": "000000010"}},
                                {"$group": {"_id": "$tcpflags", "count": {"$sum": 1}}}])
    print list(result)
    conn.close()


def find_latest_flow(tenant_id):
    conn = MongoHelper().getconn()
    db = conn["flowdb"]
    for item in db.flow.find({"project_id": "fab30037b2d54be484520cd16722f63c", "instance_id": "8e47f827-5ddd-4ee0-b043-0bece7fa3431"}).limit(10).sort("timestap", pymongo.DESCENDING):
        ltime = time.localtime(item["timestap"]/1000)
        timeStr = time.strftime("%Y-%m-%d %H:%M:%S", ltime)
        print timeStr
        print item
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    conn.close()


if __name__ == "__main__":
    get_tenant_top_src_ip("tt")
    get_tenant_top_dst_ip("tt")
    get_instance_top_src_ip("dd", "dd")
    get_instance_top_dst_ip("dd", "dd")
    get_instance_top_src_port("dd", "dd")
    get_instance_top_dst_port("dd", "dd")
    get_tenant_top_instance("dddd")

    get_instance_tcpflags_syn_flood("dd", "dd")
    # find_latest_flow("dd")

