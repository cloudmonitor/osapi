# _*_ coding:utf-8 _*_

from osapi.settings import *
KEYSTONE_ENDPOINT_ADMIN = "http://controller:35357/v2.0"

def get_all_tenants(token_id):
    """获得所有的租户信息，并进行过滤掉service项目"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = KEYSTONE_ENDPOINT_ADMIN + "/tenants"
    r = requests.get(url=url, headers=headers)
    tenants = r.json()
    del_tenants = []
    for tenant in tenants["tenants"]:
        if tenant["name"] == "service":
            del_tenants.append(tenant)
    for del_tenant in del_tenants:
        tenants["tenants"].remove(del_tenant)
    return tenants


def create_tenant(token_id, data):
    """创建租户"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = KEYSTONE_ENDPOINT_ADMIN + "/tenants"
    r = requests.post(url=url, data=data, headers=headers)
    return r.json()


def delete_tenant(token_id, tenant_id):
    """删除指定ID的租户"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = KEYSTONE_ENDPOINT_ADMIN + "/tenants/" + tenant_id
    r = requests.delete(url=url, headers=headers)
    return r.json()


def update_tenant(token_id, tenant_id, data):
    """更新租户信息"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = KEYSTONE_ENDPOINT_ADMIN + "/tenants/" + tenant_id
    r = requests.post(url=url, data=data, headers=headers)
    return r.json()


def update_tenant_quota(token_id, admin_tenant_id, tenant_id, data):
    """更新租户信息"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT + "/" + admin_tenant_id + "/os-quota-sets/" + tenant_id
    r = requests.post(url=url, data=data, headers=headers)
    return r.json()


def get_tenant_users(token_id, tenant_id):
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = KEYSTONE_ENDPOINT_ADMIN + "/tenants/" + tenant_id + "/users"
    r = requests.get(url=url, headers=headers)
    return r.json()


def get_all_users(token_id):
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = KEYSTONE_ENDPOINT_ADMIN + "/users"
    r = requests.get(url=url, headers=headers)
    users = r.json()
    del_users = []
    for user in users["users"]:
        if user["name"] == "nova":
            del_users.append(user)
        elif user["name"] == "ceilometer":
            del_users.append(user)
        elif user["name"] == "neutron":
            del_users.append(user)
        elif user["name"] == "glance":
            del_users.append(user)
    for del_user in del_users:
        users["users"].remove(del_user)
    return users


def create_user(token_id, data):
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = KEYSTONE_ENDPOINT_ADMIN + "/users"
    r = requests.post(url=url, data=data, headers=headers)
    return r.json()


if __name__ == "__main__":
    tenant = {
        "tenant": {
            "name": "test",
            "description": "A description ...",
            "enabled": True
        }
    }

    # print json.dumps(get_all_tenants("0b64851e26ed43c4a6f168c59c511d1d"))
    # print json.dumps(get_all_users("0b64851e26ed43c4a6f168c59c511d1d"))
    print json.dumps(create_tenant("a7b64185cf59465ab0524b66f95a9587", json.dumps(tenant)))
