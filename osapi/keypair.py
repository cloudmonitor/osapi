# _*_ coding:utf-8 _*_

from settings import *


def get_tenant_keypairs(token_id, tenant_id):
    """获取租户的密钥对"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id)
    r = requests.get(url+'/os-keypairs', headers=headers)
    return r.json()


def create_tenant_keypair(token_id, tenant_id, data):
    """创建租户密钥对"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id)
    r = requests.post(url+'/os-keypairs', data=data, headers=headers)
    return r.json()


def delete_tenant_keypair(token_id, tenant_id, keypair_names):
    """创建租户密钥对"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    del_state = {}
    for i in range(len(keypair_names["keypair_names"])):
        url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + '/os-keypairs/' + keypair_names["keypair_names"][i]
        r = requests.delete(url, headers=headers)
        del_state[keypair_names["keypair_names"][i]] = r.status_code
    return del_state
