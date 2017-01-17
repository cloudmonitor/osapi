# _*_ coding:utf-8 _*_

from settings import *


def get_tenant_images(token_id):
    """获取租户的镜像信息"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = GLANCE_ENDPOINT + "/images"
    r = requests.get(url=url, headers=headers)
    return r.json()


def get_image_name(token_id, image_id):
    """通过image_id获取image的名字"""
    images_info = get_tenant_images(token_id)
    image_name = "unknown"
    for i in range(len(images_info["images"])):
        if image_id == images_info["images"][i]["id"]:
            image_name = images_info["images"][i]["name"]
            break
    return image_name


if __name__ == "__main__":
    from osapi.identify import get_admin_token
    admin_token = get_admin_token("admin", "admin")
    admin_token_id = admin_token['access']['token']['id']
    admin_tenant_id = admin_token['access']['token']['tenant']['id']
    print json.dumps(get_tenant_images(admin_token_id))
    print get_image_name(admin_token_id, "add08de8-d663-4022-86a9-1b1c39a8653c")
