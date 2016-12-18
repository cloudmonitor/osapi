# _*_ coding:utf-8 _*_

from __future__ import division
import time
import pymongo

from mongodbconn import MongoHelper


def get_tenant_top_instance(tenant_id, curr_type):
    conn = MongoHelper().getconn()
    db = conn["flowdb"]
    now_time = int(time.time() * 1000)
    if curr_type == "minute":
        last_time = now_time - 10 * 60 * 1000
    elif curr_type == "hour":
        last_time = now_time - 10 * 60 * 60 * 1000
    elif curr_type == "day":
        last_time = now_time - 10 * 24 * 60 * 60 * 1000
    else:
        last_time = now_time
    result = db.flow.aggregate([{"$match": {"project_id": tenant_id,
                                            "timestap": {"$gte": last_time}}},
                                {"$group": {"_id": {"instance_id": "$instance_id", "instance_name": "$instance_name"}, "count": {"$sum": "$size"}}},
                                {"$sort": {"count": -1}},
                                {"$limit": 5}])
    conn.close()
    return list(result)


def get_tenant_top_src_ip(tenant_id, curr_type):
    conn = MongoHelper().getconn()
    db = conn["flowdb"]
    now_time = int(time.time() * 1000)
    if curr_type == "minute":
        last_time = now_time - 10 * 60 * 1000
    elif curr_type == "hour":
        last_time = now_time - 10 * 60 * 60 * 1000
    elif curr_type == "day":
        last_time = now_time - 10 * 24 * 60 * 60 * 1000
    else:
        last_time = now_time
    result = db.flow.aggregate([{"$match": {"project_id": tenant_id,
                                            "timestap": {"$gte": last_time}}},
                                {"$group": {"_id": "$ipsource", "count": {"$sum": 1}}},
                                {"$sort": {"count": -1}},
                                {"$limit": 10}])
    conn.close()
    return list(result)


def get_tenant_top_dst_ip(tenant_id, curr_type):
    conn = MongoHelper().getconn()
    db = conn["flowdb"]
    now_time = int(time.time() * 1000)
    if curr_type == "minute":
        last_time = now_time - 10 * 60 * 1000
    elif curr_type == "hour":
        last_time = now_time - 10 * 60 * 60 * 1000
    elif curr_type == "day":
        last_time = now_time - 10 * 24 * 60 * 60 * 1000
    else:
        last_time = now_time
    result = db.flow.aggregate([{"$match": {"project_id": tenant_id,
                                            "timestap": {"$gte": last_time}}},
                                {"$group": {"_id": "$ipdestination", "count": {"$sum": 1}}},
                                {"$sort": {"count": -1}},
                                {"$limit": 10}])
    conn.close()
    return list(result)


def get_instance_top_src_ip(tenant_id, instance_id, curr_type):
    conn = MongoHelper().getconn()
    db = conn["flowdb"]
    now_time = int(time.time() * 1000)
    if curr_type == "minute":
        last_time = now_time - 10 * 60 * 1000
    elif curr_type == "hour":
        last_time = now_time - 10 * 60 * 60 * 1000
    elif curr_type == "day":
        last_time = now_time - 10 * 24 * 60 * 60 * 1000
    else:
        last_time = now_time
    result = db.flow.aggregate([{"$match": {"project_id": tenant_id,
                                            "instance_id": instance_id,
                                            "timestap": {"$gte": last_time}}},
                                {"$group": {"_id": "$ipsource", "count": {"$sum": 1}}},
                                {"$sort": {"count": -1}},
                                {"$limit": 10}])
    conn.close()
    return list(result)


def get_instance_top_dst_ip(tenant_id, instance_id, curr_type):
    conn = MongoHelper().getconn()
    db = conn["flowdb"]
    now_time = int(time.time() * 1000)
    if curr_type == "minute":
        last_time = now_time - 10 * 60 * 1000
    elif curr_type == "hour":
        last_time = now_time - 10 * 60 * 60 * 1000
    elif curr_type == "day":
        last_time = now_time - 10 * 24 * 60 * 60 * 1000
    else:
        last_time = now_time
    result = db.flow.aggregate([{"$match": {"project_id": tenant_id,
                                            "instance_id": instance_id,
                                            "timestap": {"$gte": last_time}}},
                                {"$group": {"_id": "$ipdestination", "count": {"$sum": 1}}},
                                {"$sort": {"count": -1}},
                                {"$limit": 10}])
    conn.close()
    return list(result)


def get_instance_top_src_port(tenant_id, instance_id, curr_type):
    conn = MongoHelper().getconn()
    db = conn["flowdb"]
    now_time = int(time.time() * 1000)
    if curr_type == "minute":
        last_time = now_time - 10 * 60 * 1000
    elif curr_type == "hour":
        last_time = now_time - 10 * 60 * 60 * 1000
    elif curr_type == "day":
        last_time = now_time - 10 * 24 * 60 * 60 * 1000
    else:
        last_time = now_time
    result = db.flow.aggregate([{"$match": {"project_id": tenant_id,
                                            "instance_id": instance_id,
                                            "timestap": {"$gte": last_time},
                                            "ipprotocol": {"$in": [6, 17]}}},
                                {"$group": {"_id": "$srcport_or_icmptype", "count": {"$sum": 1}}},
                                {"$sort": {"count": -1}},
                                {"$limit": 10}])
    conn.close()
    return list(result)


def get_instance_top_dst_port(tenant_id, instance_id, curr_type):
    conn = MongoHelper().getconn()
    db = conn["flowdb"]
    now_time = int(time.time() * 1000)
    if curr_type == "minute":
        last_time = now_time - 10 * 60 * 1000
    elif curr_type == "hour":
        last_time = now_time - 10 * 60 * 60 * 1000
    elif curr_type == "day":
        last_time = now_time - 10 * 24 * 60 * 60 * 1000
    else:
        last_time = now_time
    result = db.flow.aggregate([{"$match": {"project_id": tenant_id,
                                            "instance_id": instance_id,
                                            "timestap": {"$gte": last_time},
                                            "ipprotocol": {"$in": [6, 17]}}},
                                {"$group": {"_id": "$dstport_or_icmpcode", "count": {"$sum": 1}}},
                                {"$sort": {"count": -1}},
                                {"$limit": 10}])
    conn.close()
    return list(result)


def get_instance_tcpflags_syn_flood(tenant_id, instance_id, curr_type):
    conn = MongoHelper().getconn()
    db = conn["flowdb"]
    now_time = int(time.time() * 1000)
    if curr_type == "minute":
        last_time = now_time - 10 * 60 * 1000
    elif curr_type == "hour":
        last_time = now_time - 10 * 60 * 60 * 1000
    elif curr_type == "day":
        last_time = now_time - 10 * 24 * 60 * 60 * 1000
    else:
        last_time = now_time
    result = db.flow.aggregate([{"$match": {"project_id": tenant_id,
                                            "instance_id": instance_id,
                                            "timestap": {"$gte": last_time},
                                            "ipprotocol": 6,
                                            "tcpflags": "000000010"}},
                                {"$group": {"_id": "$tcpflags", "count": {"$sum": 1}}}])
    conn.close()
    return list(result)


def find_latest_flow(tenant_id, instance_id):
    conn = MongoHelper().getconn()
    db = conn["flowdb"]
    result = db.flow.find({"project_id": tenant_id, "instance_id": instance_id}).\
                        limit(10).\
                        sort("timestap", pymongo.DESCENDING)
    conn.close()
    return list(result)


if __name__ == "__main__":
    # get_tenant_top_src_ip("tt")
    # get_tenant_top_dst_ip("tt")
    # get_instance_top_src_ip("dd", "dd")
    # get_instance_top_dst_ip("dd", "dd")
    # get_instance_top_src_port("dd", "dd")
    # get_instance_top_dst_port("fab30037b2d54be484520cd16722f63c", "b18ff7c9-70cc-4781-ad31-af9845e005db")
    import json
    print json.dumps(get_tenant_top_instance("fab30037b2d54be484520cd16722f63c", "minute"))

    # get_instance_tcpflags_syn_flood("fab30037b2d54be484520cd16722f63c", "b18ff7c9-70cc-4781-ad31-af9845e005db")
    # print find_latest_flow("fab30037b2d54be484520cd16722f63c", "b18ff7c9-70cc-4781-ad31-af9845e005db")

