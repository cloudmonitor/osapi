# _*_ coding:utf-8 _*_
from osapi.quota import get_tenant_used_info
from osapi.settings import *
from osapi.floatingip import get_floating_ips
from osapi.identify import get_admin_token
from osapi.securitygroup import get_security_groups, get_security_groups_rules
from osapi.neutron import *
from cloud_instance import get_all_tenant_instances
from tenant_user import get_tenant_neutron_quota


def get_tenant_compute_limits(admin_token_id, admin_tenant_id, project_id):
    """超级管理员下获取租户计算方面的配额"""
    headers = {"Content-type": "application/json", "X-Auth-Token": admin_token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=admin_tenant_id)
    r = requests.get(url+'/os-quota-sets/'+project_id, headers=headers)
    tenant_compute_limits_info = r.json()
    tenant_compute_limit = {}
    tenant_compute_limit["ram"] = tenant_compute_limits_info["quota_set"]["ram"]
    tenant_compute_limit["cores"] = tenant_compute_limits_info["quota_set"]["cores"]
    tenant_compute_limit["instances"] = tenant_compute_limits_info["quota_set"]["instances"]
    return tenant_compute_limit


def _admin_get_tenant_subnets_used(admin_token_id, project_id):
    """超级管理下根据项目id获取某一租户子网的使用个数"""
    all_subnet_info = get_tenant_subnets(admin_token_id)
    subnet_used = 0
    for i in range(len(all_subnet_info["subnets"])):
        if project_id == all_subnet_info["subnets"][i]["tenant_id"]:
            subnet_used = subnet_used + 1
    return subnet_used


def _admin_get_tenant_networks_used(admin_token_id, project_id):
    """超级管理下根据项目id获取某一租户网络的使用个数"""
    all_network_info = get_all_networks(admin_token_id)
    network_used = 0
    for i in range(len(all_network_info["networks"])):
        if project_id == all_network_info["networks"][i]["tenant_id"]:
            network_used = network_used + 1
    return network_used


def _admin_get_tenant_floatingips_used(admin_token_id, project_id):
    """超级管理下根据项目id获取某一租户floatingip的使用个数"""
    floating_ip_info = get_floating_ips(admin_token_id)
    floating_ip_used = 0
    for i in range(len(floating_ip_info["floatingips"])):
        if project_id == floating_ip_info["floatingips"][i]["tenant_id"] and "ACTIVE" == floating_ip_info["floatingips"][i]["status"]:
            floating_ip_used = floating_ip_used + 1
    return floating_ip_used


def _admin_get_tenant_security_groups(admin_token_id, project_id):
    """超级管理下根据项目id获取某一租户安全组的使用个数"""
    all_security_groups_info = get_security_groups(admin_token_id)
    security_groups_used = 0
    for i in range(len(all_security_groups_info["security_groups"])):
        if project_id == all_security_groups_info["security_groups"][i]["tenant_id"]:
            security_groups_used = security_groups_used + 1
    return security_groups_used


def _admin_get_tenant_security_groups_rule(admin_token_id, project_id):
    """超级管理下根据项目id获取某一租户安全组规则的使用个数"""
    all_security_groups_rule_info = get_security_groups_rules(admin_token_id)
    security_groups_rule_used = 0
    for i in range(len(all_security_groups_rule_info["security_group_rules"])):
        if project_id == all_security_groups_rule_info["security_group_rules"][i]["tenant_id"]:
            security_groups_rule_used = security_groups_rule_used + 1
    return security_groups_rule_used


def _admin_get_tenant_router(admin_token_id, project_id):
    """超级管理下根据项目id获取某一租户路由的使用个数"""
    all_router_info = get_tenant_routers(admin_token_id)
    router_used = 0
    for i in range(len(all_router_info["routers"])):
        if project_id == all_router_info["routers"][i]["tenant_id"]:
            router_used = router_used + 1
    return router_used


def _admin_get_tenant_ports(admin_token_id, project_id):
    """超级管理下根据项目id获取某一租户路由的使用个数"""
    all_port_info = get_tenant_ports(admin_token_id)
    ports_used = 0
    for i in range(len(all_port_info["ports"])):
        if project_id == all_port_info["ports"][i]["tenant_id"]:
            ports_used = ports_used + 1
    return ports_used


def _admin_get_tenant_static(admin_token_id,admin_tenant_id,project_id):
    """超级管理获取租户的云主机、虚拟内核、内存使用情况"""
    headers = {"Content-type": "application/json", "X-Auth-Token": admin_token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=admin_tenant_id)
    r = requests.get(url=url + "/os-simple-tenant-usage?detailed=1", headers=headers)
    tenant_usage_info = r.json()   # 获取整体的数据
    tenant_abstract = {}
    for i in range(len(tenant_usage_info["tenant_usages"])):
        memory_mb = 0
        vcpus = 0
        instance_num = 0
        if project_id == tenant_usage_info["tenant_usages"][i]["tenant_id"]:
            tenant_single_info = tenant_usage_info["tenant_usages"][i]
            for j in range(len(tenant_single_info["server_usages"])):
                memory_mb = memory_mb + tenant_single_info["server_usages"][j]["memory_mb"]
                vcpus = vcpus + tenant_single_info["server_usages"][j]["vcpus"]
                instance_num = instance_num + 1
        tenant_abstract["memory_mb"] = memory_mb
        tenant_abstract["instance_num"] = instance_num
        tenant_abstract["vcpus"] = vcpus
        break
    return tenant_abstract


def get_tenant_usage_abstract(admin_token_id, admin_tenant_id, project_id):
    """获取租户资源使用情况概览"""
    tenant_limit = {}  # 用于保存租户计算和网络方面的配额信息
    tenant_limit_compute = get_tenant_compute_limits(admin_token_id, admin_tenant_id, project_id)
    tenant_limit_network = get_tenant_neutron_quota(admin_token_id, project_id)
    tenant_limit_tmp = dict(tenant_limit_compute, **tenant_limit_network["quota"])
    tenant_limit["quotas"] = tenant_limit_tmp
    tenant_limit["subnets_used"] = _admin_get_tenant_subnets_used(admin_token_id, project_id)
    tenant_limit["networks_used"] = _admin_get_tenant_networks_used(admin_token_id, project_id)
    tenant_limit["floatingips_used"] = _admin_get_tenant_floatingips_used(admin_token_id, project_id)
    tenant_limit["security_groups_used"] = _admin_get_tenant_security_groups(admin_token_id, project_id)
    tenant_limit["security_groups_rule_used"] = _admin_get_tenant_security_groups_rule(admin_token_id, project_id)
    tenant_limit["routers_used"] = _admin_get_tenant_router(admin_token_id, project_id)
    tenant_limit["ports_used"] = _admin_get_tenant_ports(admin_token_id, project_id)
    tenant_tmp = _admin_get_tenant_static(admin_token_id, admin_tenant_id, project_id)
    tenant_limit_static = dict(tenant_limit, **tenant_tmp)
    return tenant_limit_static


def get_tenant_instances(admin_token_id, admin_tenant_id, project_id):
    """超级管理员获取租户下的所有虚拟机"""
    tenant_instances = {}
    tenant_instances["servers"] = []
    all_tenant_instances_info = get_all_tenant_instances(admin_token_id, admin_tenant_id)
    for i in range(len(all_tenant_instances_info["servers"])):
        if project_id == all_tenant_instances_info["servers"][i]["tenant_id"]:
            tenant_instances["servers"].append(all_tenant_instances_info["servers"][i])
    return tenant_instances


def get_tenant_networks(admin_token_id, project_id):
    """超级管理获取租户的网络基本情况，返回租户下所有的网络和对应的子网"""
    tenant_network_info = {}
    tenant_network_info["networks"] = []
    all_network_info = get_all_networks(admin_token_id)
    for i in range(len(all_network_info["networks"])):
        if project_id == all_network_info["networks"][i]["tenant_id"]:
            network_info_tmp = copy.deepcopy(all_network_info["networks"][i])
            for j in range(len(all_network_info["networks"][i]["subnets"])):
                subnet_id = all_network_info["networks"][i]["subnets"][j]
                subnet_info = get_subnets_info(admin_token_id, subnet_id)
                network_info_tmp["subnets"].remove(subnet_id)
                network_info_tmp["subnets"].append(subnet_info)
            tenant_network_info["networks"].append(network_info_tmp)
    return tenant_network_info


def get_tenant_routers_info(admin_token_id, project_id):
    """获取租户下所有的路由器"""
    tenant_routers = {}
    tenant_routers["routers"] = []
    all_tenant_routers = get_tenant_routers(admin_token_id)
    for i in range(len(all_tenant_routers["routers"])):
        if project_id == all_tenant_routers["routers"][i]["tenant_id"]:
            tenant_routers["routers"].append(all_tenant_routers["routers"][i])
    return tenant_routers


if __name__ == "__main__":
    admin_json = get_admin_token("admin", "admin")
    admin_tenant_id = admin_json['access']['token']['tenant']['id']
    admin_token_id = admin_json['access']['token']['id']
    # print json.dumps(get_admin_tenant_limits(admin_token_id, admin_tenant_id, "fab30037b2d54be484520cd16722f63c"))
    print json.dumps(get_tenant_usage_abstract(admin_token_id,admin_tenant_id, "676d2619d151466e9d1da24b37a61e74"))
    # print json.dumps(get_all_tenant_instances(admin_token_id, admin_tenant_id))
    # print json.dumps(get_tenant_instances(admin_token_id, admin_tenant_id, "fab30037b2d54be484520cd16722f63c"))
    # print json.dumps(get_tenant_routers_info(admin_token_id, "fab30037b2d54be484520cd16722f63c"))