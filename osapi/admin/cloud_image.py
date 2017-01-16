# _*_ coding:utf-8 _*_


from osapi.settings import *


def get_all_images(token_id):
    """获取所有的镜像信息"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = GLANCE_ENDPOINT + "/images"
    r = requests.get(url=url, headers=headers)
    return r.json()


def create_image(token_id, data):
    """上传创建镜像信息"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = GLANCE_ENDPOINT + "/images"
    # TODO
    r = requests.post(url=url, data=data, headers=headers)
    return r.json()

