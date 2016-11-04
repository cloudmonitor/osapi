# _*_ coding:utf-8 _*_

from flask import request
from settings import *
from floatingip import get_floating_ips
from securitygroup import get_security_groups, get_security_groups_rules
from identify import get_admin_token
from neutron import get_tenant_ports, get_tenant_networks, get_tenant_routers, get_tenant_subnets


def get_tenant_limits(token_id, tenant_id):
    """获取租户的资源配额限制"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id)
    r = requests.get(url+'/limits', headers=headers)
    limits = r.json()
    limits["limits"]["absolute"]["totalFloatingIpsUsed"] = _get_tenant_floatingips_used(token_id, tenant_id)
    limits["limits"]["absolute"]["totalSecurityGroupsUsed"] = _get_tenant_securitygroups_used(token_id)
    return limits


def _get_tenant_floatingips_used(token_id, tenant_id):
    """获取当前租户创建了多少floatingip"""
    floatingips = get_floating_ips(token_id)
    return len(floatingips["floatingips"])


def _get_tenant_securitygroups_used(token_id):
    """获取当前租户创建了多少安全组"""
    security_groups = get_security_groups(token_id)
    return len(security_groups["security_groups"])


def _get_tenant_securitygroups_rules_used(token_id):
    """获取当前租户创建了多少安全组规则"""
    securitygroups_rules = get_security_groups_rules(token_id)
    return len(securitygroups_rules["security_group_rules"])


def _get_compute_quota(tenant_id):
    """根据租户id获取计算方面的配额"""
    compute_quota = {}
    admin_token_id = get_admin_token()['access']['token']['id']
    headers = {"Content-type": "application/json", "X-Auth-Token": admin_token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT01+'/os-quota-sets/'+tenant_id + '/detail'
    r = requests.get(url, headers=headers)
    compute_quota_list = r.json()
    compute_quota['cores'] = compute_quota_list['quota_set']['cores']['limit']
    compute_quota['instances'] = compute_quota_list['quota_set']['instances']['limit']
    compute_quota['ram'] = compute_quota_list['quota_set']['ram']['limit']
    return compute_quota


def _get_network_quota(tenant_id):
    """根据获取所有网络方面的配额"""
    admin_token_id = get_admin_token()['access']['token']['id']
    headers = {"Content-type": "application/json", "X-Auth-Token": admin_token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT+'/quotas'
    r = requests.get(url, headers=headers)
    network_info_list = r.json()
    for i in range(len(network_info_list['quotas'])):
        if tenant_id == network_info_list['quotas'][i]['tenant_id']:
            network_info = network_info_list['quotas'][i]
            break
    return network_info


def get_tenant_quota(tenant_id):
    """获取跟租户相关的配额信息"""
    tenant_quota_info = {}
    compute_info = _get_compute_quota(tenant_id)
    network_info = _get_network_quota(tenant_id)
    del network_info['tenant_id']
    del network_info['rbac_policy']
    del network_info['subnetpool']
    tenant_quota = dict(network_info, **compute_info)
    tenant_quota_info['total'] = tenant_quota
    return tenant_quota_info


def get_tenant_used_info(token_id, tenant_id):
    """获取租户使用的信息"""
    tenant_used_info = {}
    tenant_used = {}
    tenant_used_info["network"] = len(get_tenant_networks(token_id)['networks'])
    tenant_used_info["subnet"] = len(get_tenant_subnets(token_id)['subnets'])
    tenant_used_info["router"] = len(get_tenant_routers(token_id)['routers'])
    tenant_used_info["port"] = len(get_tenant_ports(token_id)['ports'])
    tenant_used_info["security_group_rule"] = _get_tenant_securitygroups_rules_used(token_id)
    tenant_limits = get_tenant_limits(token_id, tenant_id)
    tenant_used_info["instances"] = tenant_limits['limits']['absolute']['totalInstancesUsed']
    tenant_used_info["floatingip"] = tenant_limits['limits']['absolute']['totalFloatingIpsUsed']
    tenant_used_info["security_group"] = tenant_limits['limits']['absolute']['totalSecurityGroupsUsed']
    tenant_used_info["cores"] = tenant_limits['limits']['absolute']['totalCoresUsed']
    tenant_used_info["ram"] = tenant_limits['limits']['absolute']['totalRAMUsed']
    tenant_used['used'] = tenant_used_info
    tenant_info = get_tenant_quota(tenant_id)
    tenant_quota_used = dict(tenant_used, **tenant_info)
    return json.dumps(tenant_quota_used)



