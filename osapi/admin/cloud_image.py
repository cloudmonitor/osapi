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


def delete_image(admin_token_id,images_id_list):
    """删除云镜像"""
    images_id_list = json.loads(images_id_list)
    delete_status = {}
    headers = {"Content-type": "application/json", "X-Auth-Token": admin_token_id, "Accept": "application/json"}
    for i in range(len(images_id_list["images_ids"])):
        url = GLANCE_ENDPOINT + "/images/"+images_id_list["images_ids"][i]
        r = requests.delete(url=url, headers=headers)
        delete_status[images_id_list["images_ids"][i]] = r.status_code
    return delete_status


def update_image(admin_token_id,image_id,data):
    """更新云镜像"""
    headers = {"Content-type": "application/openstack-images-v2.1-json-patch", "X-Auth-Token": admin_token_id, "Accept": "application/json"}
    url = GLANCE_ENDPOINT + "/images/"+image_id
    r = requests.patch(url=url, headers=headers, data=data)
    return r.json()
