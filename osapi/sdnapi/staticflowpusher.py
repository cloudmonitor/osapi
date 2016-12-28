# _*_ coding:utf-8 _*_

import requests

from settings import *


class StaticFlowPusher(object):

    def __init__(self, baseurl):
        self.baseurl = baseurl

    def get_flow(self, switch):
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        url = self.baseurl + "/wm/staticentrypusher/list/" + switch + "/json"
        ret = requests.get(url, headers=headers)
        return ret.json()

    def add_flow(self, data):
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        url = self.baseurl + "/wm/staticentrypusher/json"
        ret = requests.post(url, data=data, headers=headers)
        return ret.status_code == 200

    def delete_flow(self, data):
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        url = self.baseurl + "/wm/staticentrypusher/json"
        ret = requests.delete(url, data=data, headers=headers)
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