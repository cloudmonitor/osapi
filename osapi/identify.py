# _*_ coding:utf-8 _*_

"""主要用来用户认证以及租户获取"""

from settings import *


def get_user_token(username, password):
    """获取指定用户名密码的TOKEN,返回json"""
    credential = CREDENTIAL_PASSWORD % ('', username, password)
    headers = {"Content-type": "application/json", "Accept": "application/json"}
    r = requests.post(KEYSTONE_ENDPOINT+'/tokens', data=credential, headers=headers)
    return r.json()


def get_admin_token():
    """"获取admin的token"""
    credential = CREDENTIAL_PASSWORD % ('admin', 'admin', 'admin')
    headers = {"Content-type": "application/json", "Accept": "application/json"}
    r = requests.post(KEYSTONE_ENDPOINT+'/tokens', data=credential, headers=headers)
    return r.json()


def get_tenant_token(tenantname, token):
    """获取指定租户、用户名、密码的TOKEN,返回json"""
    credential = CREDENTIAL_TOKEN % (tenantname, token)
    headers = {"Content-type": "application/json", "Accept": "application/json"}
    r = requests.post(KEYSTONE_ENDPOINT+'/tokens', data=credential, headers=headers)
    response_json = r.json()
    return response_json


def get_tenants(token_id):
    """获取指定TOKEN下的所有租户，返回一个租户字典,通过['tenants'][0 1 ... n]['id']取得租户id,返回样例如下"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    r = requests.get(KEYSTONE_ENDPOINT+'/tenants', headers=headers)
    return r.json()



