# _*_ coding:utf-8 _*_

from __future__ import division
import time

from mongodbconn import MongoHelper
from settings import *


def get_tenant_top_instance(tenant_id, curr_type):
    """统计最近流量中虚拟机 TOP 5"""
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


def get_tenant_top_protocol(tenant_id, curr_type):
    """统计最近流量中协议TOP 5"""
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
                                {"$group": {"_id": "$ipprotocol", "count": {"$sum": 1}}},
                                {"$sort": {"count": -1}},
                                {"$limit": 5}])
    conn.close()
    return list(result)


def get_tenant_top_ip(tenant_id, curr_type):
    """统计最近流量中IP-TOP 10"""
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


def get_tenant_top_port(tenant_id, curr_type):
    """统计最近流量中PORT-TOP 10"""
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
                                            "timestap": {"$gte": last_time},
                                            "ipprotocol": {"$in": [6, 17]}}},
                                {"$group": {"_id": "$srcport_or_icmptype", "count": {"$sum": 1}}},
                                {"$sort": {"count": -1}},
                                {"$limit": 10}])
    conn.close()
    return list(result)


def get_tenant_top_protocol_port(tenant_id, curr_type):
    """统计最近流量中PORT-TOP 10"""
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
                                {"$group": {"_id": {"ipprotocol": "$ipprotocol", "dstport_or_icmpcode": "$dstport_or_icmpcode"},
                                            "count": {"$sum": 1}}},
                                {"$sort": {"count": -1}},
                                {"$limit": 10}])
    conn.close()
    return list(result)


def get_tenant_top_ip_link(tenant_id, curr_type):
    """统计最近流量源IP-目的IP-TOP 10"""
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
                                {"$group": {"_id": {"ipsource": "$ipsource", "ipdestination": "$ipdestination"},
                                            "count": {"$sum": "$size"}}},
                                {"$sort": {"count": -1}},
                                {"$limit": 10}])
    conn.close()
    return list(result)


def get_tenant_top_session(tenant_id, curr_type):
    """统计最近流量SESSION-TOP 10"""
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
                                {"$group": {"_id": {"ipsource": "$ipsource", "ipdestination": "$ipdestination",
                                                    "srcport_or_icmptype": "$srcport_or_icmptype",
                                                    "dstport_or_icmpcode": "$dstport_or_icmpcode",
                                                    "ipprotocol": "$ipprotocol"},
                                            "count": {"$sum": "$size"}}},
                                {"$sort": {"count": -1}},
                                {"$limit": 10}])
    conn.close()
    return list(result)


def get_instance_top_ip_link(tenant_id, instance_id, curr_type):
    """统计最近流量源IP-目的IP-TOP 10"""
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
                                {"$group": {"_id": {"ipsource": "$ipsource", "ipdestination": "$ipdestination"},
                                            "count": {"$sum": "$size"}}},
                                {"$sort": {"count": -1}},
                                {"$limit": 10}])
    conn.close()
    return list(result)


def get_instance_top_protocol_port(tenant_id, instance_id, curr_type):
    """统计最近流量中PORT-TOP 10"""
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
                                {"$group": {"_id": {"ipprotocol": "$ipprotocol", "srcport_or_icmptype": "$srcport_or_icmptype"},
                                            "count": {"$sum": 1}}},
                                {"$sort": {"count": -1}},
                                {"$limit": 10}])
    conn.close()
    return list(result)


def get_instance_top_session(tenant_id, instance_id, curr_type):
    """统计最近流量SESSION-TOP 10"""
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
                                {"$group": {"_id": {"ipsource": "$ipsource", "ipdestination": "$ipdestination",
                                                    "srcport_or_icmptype": "$srcport_or_icmptype",
                                                    "dstport_or_icmpcode": "$dstport_or_icmpcode",
                                                    "ipprotocol": "$ipprotocol"},
                                            "count": {"$sum": "$size"}}},
                                {"$sort": {"count": -1}},
                                {"$limit": 10}])
    conn.close()
    return list(result)


def get_instance_top_src_ip(tenant_id, instance_id, curr_type):
    """统计虚拟机源IP--TOP 10"""
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
                                            # "macsource": {"$ne": mac_addr},
                                            "timestap": {"$gte": last_time}}},
                                {"$group": {"_id": "$ipsource", "count": {"$sum": 1}}},
                                {"$sort": {"count": -1}},
                                {"$limit": 10}])
    conn.close()
    return list(result)


def get_instance_top_dst_ip(tenant_id, instance_id, curr_type):
    """统计虚拟机目的IP--TOP 10"""
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
                                            # "macdestination": {"$ne": mac_addr},
                                            "timestap": {"$gte": last_time}}},
                                {"$group": {"_id": "$ipdestination", "count": {"$sum": 1}}},
                                {"$sort": {"count": -1}},
                                {"$limit": 10}])
    conn.close()
    return list(result)


def get_instance_top_src_port(tenant_id, instance_id, curr_type):
    """统计虚拟机源PORT--TOP 10"""
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
    """统计虚拟机目的PORT--TOP 10"""
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
                                            "ipprotocol": 6}},
                                {"$group": {"_id": "$tcpflags", "count": {"$sum": 1}}}])
    conn.close()
    return list(result)


def get_instance_active_flow(instance_id):
    """统计虚拟机最近活动流- TOP 10"""
    url = ACTIVE_FLOW_URL % (instance_id, )
    ret = requests.get(url)
    if ret.status_code == 200:
        return ret.json()
    else:
        return {"status": "error"}


if __name__ == "__main__":

    import json
    # print json.dumps(get_tenant_top_instance("fab30037b2d54be484520cd16722f63c", "minute"))
    # print json.dumps(get_tenant_top_ip("fab30037b2d54be484520cd16722f63c", "minute"))
    # print json.dumps(get_tenant_top_protocol_port("fab30037b2d54be484520cd16722f63c", "minute"))

    # print get_instance_tcpflags_syn_flood("fab30037b2d54be484520cd16722f63c", "b18ff7c9-70cc-4781-ad31-af9845e005db",
    # "minute")
    # print find_latest_flow("fab30037b2d54be484520cd16722f63c", "b18ff7c9-70cc-4781-ad31-af9845e005db")

    print get_instance_active_flow("b18ff7c9-70cc-4781-ad31-af9845e005db")

