# _*_ coding:utf-8 _*_

from osapi.quota import get_tenant_used_info
from osapi.settings import *
from osapi.floatingip import get_floating_ips
from osapi.identify import get_admin_token
from osapi.securitygroup import get_security_groups, get_security_groups_rules
from osapi.neutron import *
from osapi.flavors import get_tenant_flavors, get_flavor_name
from osapi.images import get_tenant_images, get_image_name
from tenant_user import get_tenant_neutron_quota, get_tenant_name, get_all_tenants


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


def _admin_get_tenant_static(admin_token_id, admin_tenant_id, project_id):
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


def get_all_tenant_usage(admin_token_id, admin_tenant_id):
    """获取所有租户的资源使用概览"""
    all_tenants_usage_info = {}
    all_tenants_usage_info["tenants_usage_info"] = []
    tenants_info = get_all_tenants(admin_token_id)
    for tenant in tenants_info["tenants"]:
        tenant_usage_info = get_tenant_usage_abstract(admin_token_id, admin_tenant_id, tenant["id"])
        tenant_usage_info["id"] = tenant["id"]
        tenant_usage_info["name"] = tenant["name"]
        tenant_usage_info["description"] = tenant["description"]
        tenant_usage_info["enabled"] = tenant["enabled"]
        all_tenants_usage_info["tenants_usage_info"].append(tenant_usage_info)
    return all_tenants_usage_info


def get_tenant_instances(admin_token_id, admin_tenant_id, project_id):
    """超级管理员获取租户下的所有虚拟机"""
    headers = {"Content-type": "application/json", "X-Auth-Token": admin_token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=admin_tenant_id)
    r = requests.get(url + '/servers/detail?all_tenants=1&tenant_id=' + project_id, headers=headers)
    instances_info = r.json()
    flavors_info = get_tenant_flavors(admin_token_id, admin_tenant_id)
    images_info = get_tenant_images(admin_token_id)
    # 获取租户名
    tenants_info = get_all_tenants(admin_token_id)
    tenant_name = get_tenant_name(project_id, tenants_info)
    for i in range(len(instances_info['servers'])):
        # 获取实例端口详情
        ret = requests.get(url + '/servers/' + instances_info['servers'][i]['id'] + "/os-interface", headers=headers)
        instances_info['servers'][i]['interfaceAttachments'] = ret.json()['interfaceAttachments']
        # 获取实例类型名
        flavor_name = get_flavor_name(instances_info['servers'][i]["flavor"]["id"], flavors_info)
        instances_info['servers'][i]["flavor"]["flavor_name"] = flavor_name
        # 获取实例镜像名
        image_name = get_image_name(instances_info['servers'][i]["image"]["id"], images_info)
        instances_info['servers'][i]['image']['image_name'] = image_name
        # 设置实例租户名
        instances_info['servers'][i]["tenant_name"] = tenant_name
    return instances_info


def get_tenant_networks(admin_token_id, project_id):
    """超级管理获取租户的网络基本情况，返回租户下所有的网络和对应的子网"""
    tenant_network_info = {}
    tenant_network_info["networks"] = []
    headers = {"Content-type": "application/json", "X-Auth-Token": admin_token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT
    r = requests.get(url + '/networks?tenant_id=' + project_id, headers=headers)
    network_info = r.json()
    for i in range(len(network_info["networks"])):
        network_info_tmp = copy.deepcopy(network_info["networks"][i])
        for j in range(len(network_info["networks"][i]["subnets"])):
            subnet_id = network_info["networks"][i]["subnets"][j]
            subnet_info = get_subnets_info(admin_token_id, subnet_id)
            network_info_tmp["subnets"].remove(subnet_id)
            network_info_tmp["subnets"].append(subnet_info)
        tenant_network_info["networks"].append(network_info_tmp)
    return tenant_network_info


def get_tenant_routers_info(admin_token_id, project_id):
    """获取租户下所有的路由器"""
    headers = {"Content-type": "application/json", "X-Auth-Token": admin_token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT
    r = requests.get(url + '/routers?tenant_id=' + project_id, headers=headers)
    return r.json()


def admin_create_image(admin_token_id, admin_tenant_id, server_id, data):
    """根据虚拟机id来创建快照"""
    headers = {"Content-type": "application/json", "X-Auth-Token": admin_token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=admin_tenant_id) + "/servers/"+server_id+"/action"
    r = requests.post(url=url, data=data, headers=headers)
    return r.status_code


def admin_get_instance_vnc(admin_token_id, admin_tenant_id, server_id, data):
    """获取虚拟机的vnc"""
    headers = {"Content-type": "application/json", "X-Auth-Token": admin_token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=admin_tenant_id) + "/servers/"+server_id+"/action"
    r = requests.post(url=url, data=data, headers=headers)
    return r.json()


def admin_reboot_instance(admin_token_id, admin_tenant_id, server_id, data):
    """软重启、硬重启虚拟机"""
    headers = {"Content-type": "application/json", "X-Auth-Token": admin_token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=admin_tenant_id) + "/servers/"+server_id+"/action"
    r = requests.post(url=url, data=data, headers=headers)
    return r.status_code


def admin_delete_servers(token_id, tenant_id, servers_id_list):
    """终止虚拟机"""
    servers_id_list = json.loads(servers_id_list)
    delete_status = {}
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    for i in range(len(servers_id_list["servers_ids"])):
        url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/servers/" + servers_id_list["servers_ids"][i]
        r = requests.delete(url=url, headers=headers)
        delete_status[servers_id_list["servers_ids"][i]] = r.status_code
    return delete_status


if __name__ == "__main__":
    admin_json = get_admin_token("admin", "admin")
    admin_tenant_id = admin_json['access']['token']['tenant']['id']
    admin_token_id = admin_json['access']['token']['id']
    # print admin_create_image(admin_token_id, admin_tenant_id, "11515b34-6400-4444-aab7-b93fb0733979", '{"createImage" : {"name" : "foo-image"}}')
    # print json.dumps(admin_get_instance_vnc(admin_token_id, admin_tenant_id, "11515b34-6400-4444-aab7-b93fb0733979", '{"os-getVNCConsole": {"type": "novnc"}}'))
    # print admin_reboot_instance(admin_token_id, admin_tenant_id, "11515b34-6400-4444-aab7-b93fb0733979", '{"reboot" : {"type" : "SOFT"}}')
    s = '{"servers_ids":["8a95521b-d649-4572-b4cc-c72e1104bcdf","7086c89d-239b-4a9d-b806-cb0d1ba02d69"]}'
    # print type(json.loads(s))
    print json.dumps(admin_delete_servers(admin_token_id, admin_tenant_id, json.loads(s)))