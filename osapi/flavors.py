# _*_ coding:utf-8 _*_


from settings import *


def get_tenant_flavors(token_id, tenant_id):
    """获取租户的类型"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id)
    r = requests.get(url+'/flavors/detail', headers=headers)
    return r.json()


def get_flavor_name(token_id, tenant_id, flavor_id):
    """通过flavor_id获取flavor的名字"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id)
    r = requests.get(url+'/flavors', headers=headers)
    flavors_info = r.json()
    for i in range(len(flavors_info["flavors"])):
        if flavor_id == flavors_info["flavors"][i]["id"]:
            flavor_name = flavors_info["flavors"][i]["name"]
            break
    return flavor_name


if __name__ == "__main__":
    from osapi.identify import get_admin_token

    admin_token = get_admin_token("admin", "admin")
    admin_token_id = admin_token['access']['token']['id']
    admin_tenant_id = admin_token['access']['token']['tenant']['id']
    print json.dumps(get_tenant_flavors(admin_token_id, admin_tenant_id))
