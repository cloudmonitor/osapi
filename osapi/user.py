# _*_ coding:utf-8 _*_
from util import auth_is_available
from settings import *
from identify import get_admin_token


def get_users_list(admin_token_id):
    """获取用户列表"""
    headers = {"Content-type": "application/json", "X-Auth-Token": admin_token_id, "Accept": "application/json"}
    r = requests.get(url=KEYSTONE_ENDPOINT01, headers=headers)
    return r.json()


def get_users_detail(admin_token_id, user_id):
    """获取用户详情"""
    headers = {"Content-type": "application/json", "X-Auth-Token": admin_token_id, "Accept": "application/json"}
    url = KEYSTONE_ENDPOINT01 + '/'+user_id
    r = requests.get(url=url, headers=headers)
    return r.json()


@auth_is_available
def update_user(user_id, user_data):
    """更新用户，包括用户名、密码、是否激活"""
    admin_token_id = get_admin_token()['access']['token']['id']
    headers = {"Content-type": "application/json", "X-Auth-Token": admin_token_id, "Accept": "application/json"}
    url = KEYSTONE_ENDPOINT01 + '/' + user_id
    r = requests.put(url=url, data=json.dumps(user_data), headers=headers)
    return r.json()


@auth_is_available
def create_user(user_data):
    """创建用户"""
    admin_token_id = get_admin_token()
    headers = {"Content-type": "application/json", "X-Auth-Token": admin_token_id, "Accept": "application/json"}
    url = KEYSTONE_ENDPOINT01
    r = requests.put(url=url, data=user_data, headers=headers)
    return r.json()


@auth_is_available
def delete_user(user_id):
    """删除用户"""
    admin_token_id = get_admin_token()
    headers = {"Content-type": "application/json", "X-Auth-Token": admin_token_id, "Accept": "application/json"}
    url = KEYSTONE_ENDPOINT01 + '/' + user_id
    r = requests.delete(url=url, headers=headers)
    return r.status_code()



# def update_user(token, user_id, user_data):
#     """更新用户，包括用户名、密码、是否激活"""
#     if auth_is_available(token):
#         admin_token_id = get_admin_token()['access']['token']['id']
#         headers = {"Content-type": "application/json", "X-Auth-Token": admin_token_id, "Accept": "application/json"}
#         url = KEYSTONE_ENDPOINT01 + '/' + user_id
#         r = requests.put(url=url, data=json.dumps(user_data), headers=headers)
#         return r.json()
#     else:
#         return json.loads('{"error":"not available"}')
#
#
# def create_user(token, user_data):
#     """创建用户"""
#     if auth_is_available(token):
#         admin_token_id = get_admin_token()
#         headers = {"Content-type": "application/json", "X-Auth-Token": admin_token_id, "Accept": "application/json"}
#         url = KEYSTONE_ENDPOINT01
#         print url
#         r = requests.put(url=url, data=user_data, headers=headers)
#         return r.json()
#     else:
#         return json.loads('{"error":"not available"}')
#
#
# def delete_user(token, user_id):
#     """删除用户"""
#     if auth_is_available(token):
#         admin_token_id = get_admin_token()
#         headers = {"Content-type": "application/json", "X-Auth-Token": admin_token_id, "Accept": "application/json"}
#         url = KEYSTONE_ENDPOINT01 + '/' + user_id
#         print url
#         r = requests.delete(url=url, headers=headers)
#         return r.status_code()
#     else:
#         return json.loads('{"error":"not available"}')