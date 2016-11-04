# _*_ coding:utf-8 _*_

from settings import *


def get_tenant_images(token_id):
    """获取租户的镜像信息"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = GLANCE_ENDPOINT + "/images"
    print url
    r = requests.get(url=url, headers=headers)
    return r.json()