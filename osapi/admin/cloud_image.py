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


if __name__ == "__main__":
    from osapi.identify import get_admin_token

    admin_token = get_admin_token("admin", "admin")
    admin_token_id = admin_token['access']['token']['id']
    admin_tenant_id = admin_token['access']['token']['tenant']['id']
    print json.dumps(get_all_images(admin_token_id))

