# _*_ coding:utf-8 _*_

import requests


class Controller(object):

    def __init__(self, baseurl):
        self.baseurl = baseurl

    def get_switches(self):
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        url = self.baseurl + "/wm/core/controller/switches/json"
        ret = requests.get(url, headers=headers)
        return ret.json()


