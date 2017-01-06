# _*_ coding:utf-8 _*_

import requests
import json
from settings import *
from osapi.mongodbconn import MongoHelper


class StaticFlowPusher(object):

    def __init__(self, baseurl):
        self.baseurl = baseurl

    def get_flow(self, tenant_id):
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        url = self.baseurl + "/wm/staticentrypusher/list/all/json"
        ret = requests.get(url, headers=headers)
        tenant_ofrules = []
        if ret.status_code == 200:
            all_ofrules = ret.json()
            conn = MongoHelper(OPENFLOWDB_CONN).getconn()
            db = conn["openflowdb"]
            for ofrule in db.ofrules.find({"tenant_id": tenant_id}, {'_id': 0}):
                for key, vals in all_ofrules.items():
                    if ofrule["flow_entry_inswitch"] == key:
                        for val in vals:
                            for k, v in val.items():
                                if k == ofrule["flow_entry_name"]:
                                    ofrule_new = dict(ofrule, **v)
                                    tenant_ofrules.append(ofrule_new)
            conn.close()
        return tenant_ofrules

    def add_flow(self, data, tenant_id, instance_id, instance_name):
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        url = self.baseurl + "/wm/staticentrypusher/json"
        ret = requests.post(url, data=data, headers=headers)
        if ret.status_code == 200:
            flow_entry = json.loads(data)
            ofrule = {}
            ofrule["tenant_id"] = tenant_id
            ofrule["flow_entry_name"] = flow_entry["name"]
            ofrule["flow_entry_inswitch"] = flow_entry["switch"]
            ofrule["instance_id"] = instance_id
            ofrule["instance_name"] = instance_name
            conn = MongoHelper(OPENFLOWDB_CONN).getconn()
            db = conn["openflowdb"]
            ofrule_one = db.ofrules.find_one({"flow_entry_name": flow_entry["name"]})
            if ofrule_one != None:
                db.ofrules.update({"flow_entry_name": flow_entry["name"]},
                                  {"$set": {"tenant_id": tenant_id,
                                            "flow_entry_inswitch": flow_entry["switch"],
                                            "instance_id": instance_id,
                                            "instance_name": instance_name}})
            else:
                db.ofrules.insert(ofrule)
            conn.close()
        return ret.status_code == 200

    def delete_flow(self, data, tenant_id):
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        url = self.baseurl + "/wm/staticentrypusher/json"
        ret = requests.delete(url, data=data, headers=headers)
        if ret.status_code == 200:
            flow_entry = json.loads(data)
            conn = MongoHelper(OPENFLOWDB_CONN).getconn()
            db = conn["openflowdb"]
            db.ofrules.remove({"tenant_id": tenant_id, "flow_entry_name": flow_entry["name"]})
            conn.close()
        return ret.status_code == 200


flow1 = {
    'switch': "00:00:00:00:00:00:00:01",
    "name": "flow_mod_1",
    "cookie": "0",
    "priority": "32768",
    "in_port": "1",
    "active": "true",
    "actions": "output=flood"
}

flow2 = {
    'switch': "00:00:00:00:00:00:00:01",
    "name": "flow_mod_2",
    "cookie": "0",
    "priority": "32768",
    "in_port": "2",
    "active": "true",
    "actions": "output=flood"
}

if __name__ == "__main__":
    print "hello world"
    conn = MongoHelper(OPENFLOWDB_CONN).getconn()
    db = conn["openflowdb"]
    ofrule = {}
    ofrule["tenant_id"] = "fab30037b2d54be484520cd16722f63c"
    ofrule["flow_entry_name"] = "test01"
    ofrule["flow_entry_inswitch"] = "00:00:72:94:fc:09:5d:43"
    ofrule["instance_id"] = "3d77c37a-a67e-43b9-a10d-f037472a5319"
    # db.ofrules.insert(ofrule)
    ofrule_one = db.ofrules.find_one({"flow_entry_name": "test02"})
    ofrule_two = db.ofrules.find_one({"flow_entry_name": "test01"})
    print dict(db.ofrules.find_one())
    if ofrule_one == None:
        print "None"
    staicflowpusher = StaticFlowPusher(BASE_URL)
    print json.dumps(staicflowpusher.get_flow("fab30037b2d54be484520cd16722f63c"))