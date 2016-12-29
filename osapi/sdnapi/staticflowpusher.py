# _*_ coding:utf-8 _*_

import requests
import json
from settings import *

from osapi.mongodbconn import MongoHelper


class StaticFlowPusher(object):

    def __init__(self, baseurl):
        self.baseurl = baseurl

    def get_flow(self, switch, tenant_id):
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        url = self.baseurl + "/wm/staticentrypusher/list/" + switch + "/json"
        ret = requests.get(url, headers=headers)
        tenant_ofrules = []
        if ret.status_code == 200:
            all_ofrules = ret.json()
            conn = MongoHelper(OPENFLOWDB_CONN).getconn()
            db = conn["openflowdb"]
            for ofrule in db.ofrules.find({"tenant_id": tenant_id}):
                for key, vals in all_ofrules.items():
                    if ofrule["flow_entry_inswitch"] == key:
                        for val in vals:
                            for k, v in val.items():
                                if k == ofrule["flow_entry_name"]:
                                    ofrule_new = dict(ofrule, **v)
                                    tenant_ofrules.append(ofrule_new)
            conn.close()
        return json.loads(tenant_ofrules)

    def add_flow(self, data, tenant_id, instance_id):
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
            conn = MongoHelper(OPENFLOWDB_CONN).getconn()
            db = conn["openflowdb"]
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

# pusher.set(flow1)
# pusher.set(flow2)