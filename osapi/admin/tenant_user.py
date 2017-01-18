# _*_ coding:utf-8 _*_

from osapi.settings import *


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
    """删除指定ID的租户，删除成功返回204"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = KEYSTONE_ENDPOINT_ADMIN + "/tenants/" + tenant_id
    r = requests.delete(url=url, headers=headers)
    return r.status_code


def delete_tanant_list(token_id, tenant_id_list):
    """删除一个列表中的项目，{"tenant_id":[,]}"""
    status_code_list = {}  # 用于存储返回值
    status_code_list["status_code"] = []
    # tenant_id_list = json.loads(tenant_id_list)
    for i in range(len(tenant_id_list["tenant_id"])):
        status_code = delete_tenant(token_id, tenant_id_list["tenant_id"][i])
        status_code_list["status_code"].append(status_code)
    return status_code_list


def update_tenant(token_id, tenant_id, data):
    """更新租户信息"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = KEYSTONE_ENDPOINT_ADMIN + "/tenants/" + tenant_id
    r = requests.post(url=url, data=data, headers=headers)
    return r.json()


def get_tenant_quota(token_id, admin_tenant_id, tenant_id):
    """获取租户配额信息"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=admin_tenant_id) + "/os-quota-sets/" + tenant_id
    r = requests.get(url=url, headers=headers)
    return r.json()


def update_tenant_quota(token_id, admin_tenant_id, tenant_id, data):
    """更新租户配额信息"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=admin_tenant_id) + "/os-quota-sets/" + tenant_id
    r = requests.post(url=url, data=data, headers=headers)
    return r.json()


def get_tenant_neutron_quota(token_id, tenant_id):
    """获取租户网络相关配额信息"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + "/quotas/" + tenant_id
    r = requests.get(url=url, headers=headers)
    return r.json()


def update_tenant_neutron_quota(token_id, tenant_id, data):
    """更新租户网络相关配额信息"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + "/quotas/" + tenant_id
    r = requests.put(url=url, data=data, headers=headers)
    return r.json()


def get_tenant_users(token_id, tenant_id):
    """获取租户的用户"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = KEYSTONE_ENDPOINT_ADMIN + "/tenants/" + tenant_id + "/users"
    r = requests.get(url=url, headers=headers)
    return r.json()


def get_tenant_user_role(token_id, tenant_id, user_id):
    """获取租户用户的角色"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = KEYSTONE_ENDPOINT_ADMIN + "/tenants/" + tenant_id + "/users/" + user_id + "/roles"
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
    """创建用户"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = KEYSTONE_ENDPOINT_ADMIN + "/users"
    r = requests.post(url=url, data=data, headers=headers)
    return r.json()


def delete_user(token_id, user_id):
    """删除用户，删除成功返回204"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = KEYSTONE_ENDPOINT_ADMIN + "/users/" + user_id
    r = requests.delete(url=url, headers=headers)
    return r.status_code


def update_user(token_id, user_id, data):
    """删除用户，删除成功返回204"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = KEYSTONE_ENDPOINT_ADMIN + "/users/" + user_id
    r = requests.post(url=url, data=data, headers=headers)
    return r.json()


if __name__ == "__main__":
    tenant = {
        "tenant": {
            "name": "test02",
            "description": "A description ...",
            "enabled": True
        }
    }
    user = {
        "user": {
            "email": "new-user@example.com",
            "password": None,
            "enabled": True,
            "name": "new-user"
        }
    }

    quota = {
      "quota": {
        "subnet": 10,
        "network": 10,
        "floatingip": 50,
        "security_group_rule": 100,
        "security_group": 10,
        "router": 10,
        "port": 50
      }
    }
    # print json.dumps(get_all_tenants("e877e05d418d48acba0483e355e16a50"))
    # print json.dumps(get_all_users("0b64851e26ed43c4a6f168c59c511d1d"))
    # print json.dumps(create_tenant("e90c0fdf0c364474b9c375a2e5a4e67d", json.dumps(tenant)))
    # print json.dumps(update_tenant("e90c0fdf0c364474b9c375a2e5a4e67d", "676d2619d151466e9d1da24b37a61e74", json.dumps(tenant)))
    # print json.dumps(create_user("e877e05d418d48acba0483e355e16a50", json.dumps(user)))
    print json.dumps(get_tenant_quota("5b35a6ff837a460a9b83577b020982c6", "5d03fc15631048d19bedaf1f911568e8", "676d2619d151466e9d1da24b37a61e74"))
    print json.dumps(get_tenant_neutron_quota("5b35a6ff837a460a9b83577b020982c6", "676d2619d151466e9d1da24b37a61e74"))


