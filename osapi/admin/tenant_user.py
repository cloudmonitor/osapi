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
        if tenant["name"] == "admin":
            del_tenants.append(tenant)
    for del_tenant in del_tenants:
        tenants["tenants"].remove(del_tenant)
    return tenants


def get_tenant_name(tenant_id, tenants_info):
    tenant_name = "unknown"
    for tenant in tenants_info["tenants"]:
        if tenant_id == tenant["id"]:
            tenant_name = tenant["name"]
            break
    return tenant_name


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
    # tenant_id_list = json.loads(tenant_id_list)
    for i in range(len(tenant_id_list["tenant_id"])):
        status_code = delete_tenant(token_id, tenant_id_list["tenant_id"][i])
        status_code_list[tenant_id_list["tenant_id"][i]] = status_code
    return status_code_list


def update_tenant(token_id, tenant_id, data):
    """更新租户信息"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = KEYSTONE_ENDPOINT_ADMIN + "/tenants/" + tenant_id
    r = requests.post(url=url, data=data, headers=headers)
    return r.json()


def get_tenant_basic_quota(token_id, admin_tenant_id, tenant_id):
    """获取租户基本配额信息"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=admin_tenant_id) + "/os-quota-sets/" + tenant_id
    r = requests.get(url=url, headers=headers)
    return r.json()


def update_tenant_basic_quota(token_id, admin_tenant_id, tenant_id, data):
    """更新租户基本配额信息"""
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
    users_info = r.json()
    for user in users_info["users"]:
        user_roles_info = get_tenant_user_role(token_id, tenant_id, user["id"])
        user["roles"] = user_roles_info["roles"]
    return users_info


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
        elif user["name"] == "admin":
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


def delete_user_list(token_id, user_id_list):
    """删除一个列表中的用户，{"user_id":[,]}"""
    status_code_list = {}  # 用于存储返回值
    # tenant_id_list = json.loads(tenant_id_list)
    for i in range(len(user_id_list["user_id"])):
        status_code = delete_user(token_id, user_id_list["user_id"][i])
        status_code_list[user_id_list["user_id"][i]] = status_code
    return status_code_list


def update_user(token_id, user_id, data):
    """删除用户，删除成功返回204"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = KEYSTONE_ENDPOINT_ADMIN + "/users/" + user_id
    r = requests.put(url=url, data=data, headers=headers)
    return r.json()


def get_all_roles(token_id):
    """获取所有的角色"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = KEYSTONE_ENDPOINT_ADMIN + "/OS-KSADM/roles"
    r = requests.get(url=url, headers=headers)
    roles = r.json()
    del_roles = []
    for role in roles["roles"]:
        if role["name"] == "admin":
            del_roles.append(role)
    for del_role in del_roles:
        roles["roles"].remove(del_role)
    return roles


def grant_tenant_user_role(token_id, tenant_id, user_id, role_id):
    """给一个租户的用户授予角色"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = KEYSTONE_ENDPOINT_ADMIN + "/tenants/" + tenant_id + "/users/" + user_id + "/roles/OS-KSADM/" + role_id
    r = requests.put(url, headers=headers)
    return r.json()


if __name__ == "__main__":
    from osapi.identify import get_admin_token

    admin_token = get_admin_token("admin", "admin")
    admin_token_id = admin_token['access']['token']['id']
    admin_tenant_id = admin_token['access']['token']['tenant']['id']
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
    # print json.dumps(get_tenant_basic_quota(admin_token_id, admin_tenant_id, "fab30037b2d54be484520cd16722f63c"))
    # print json.dumps(get_tenant_neutron_quota(admin_token_id, "fab30037b2d54be484520cd16722f63c"))
    # print json.dumps(get_tenant_users(admin_token_id, admin_tenant_id))
    user_data = {
        "user": {
            "email": "",
            "name": "1232"
            # "tenantId": "676d2619d151466e9d1da24b37a61e74"
        }
    }
    print json.dumps(update_user(admin_token_id, "4256e063bd9546e388a6db938bdd9cb1", json.dumps(user_data)))


