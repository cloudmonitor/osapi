# _*_ coding:utf-8 _*_

from settings import *


def get_security_groups(token_id):
    """列出安全组的信息"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + '/security-groups'
    r = requests.get(url, headers=headers)
    return r.json()


def create_security_group(token_id, data):
    """根据token_id和安全组名字创建安全组"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + "/security-groups"
    r = requests.post(url=url, headers=headers, data=json.dumps(data))
    return r.json()


def update_security_group(token_id, security_group, security_group_id):
    """更新安全组"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + '/security-groups/' + security_group_id
    r = requests.put(url=url, data=security_group, headers=headers)
    return r.json()


def delete_security_group(token_id, sg_id_list):
    """根据security_group_id删除安全组"""
    sg_del_status = {}
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    for i in range(len(sg_id_list["sg_ids"])):
        url = NEUTRON_ENDPOINT + "/security-groups/"+sg_id_list["sg_ids"][i]
        r = requests.delete(url=url, headers=headers)
        sg_del_status[sg_id_list["sg_ids"][i]] = r.status_code
    return sg_del_status


def get_security_groups_rules(token_id):
    """列出安全组规则的信息"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + '/security-group-rules'
    r = requests.get(url, headers=headers)
    return r.json()


def create_security_group_rules(token_id, data):
    """创建安全组规则"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + "/security-group-rules"
    r = requests.post(url=url, headers=headers, data=json.dumps(data))
    return r.json()


def delete_security_group_rules(token_id, sg_id_rules_list):
    sg_rules_del_status = {}
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    for i in range(len(sg_id_rules_list["sg_rules_ids"])):
        url = NEUTRON_ENDPOINT + "/security-group-rules/"+sg_id_rules_list["sg_rules_ids"][i]
        r = requests.delete(url=url, headers=headers)
        sg_rules_del_status[sg_id_rules_list["sg_rules_ids"][i]] = r.status_code
    return sg_rules_del_status