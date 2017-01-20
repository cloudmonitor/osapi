# _*_ coding:utf-8 _*_


from osapi.settings import *
from osapi.user import *
from osapi.nova import *
from osapi.neutron import *
from osapi.admin.cloud_instance import *
from osapi.admin.physical_host import get_hypervisor_detail
from osapi.admin.tenant_user import get_tenant_name_by_tenant_id


def get_all_usage_data(token_id, start_time, stop_time, tenant_id):
    """获取所有租户的资源使用情况"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id)
    r = requests.get(url=url + "/os-simple-tenant-usage?detailed=1&start=" + start_time + "&end="+stop_time, headers=headers)
    return r.json()


def get_tenant_usage(token_id, start_time, stop_time, tenant_id):
    """获取租户的虚拟内核、磁盘、内存以及相应的使用时间"""
    tenants_usage_info = {}  # 用于最后返回的数据
    tenants_usage_info["tenant_usages"] = []
    usage_info = get_all_usage_data(token_id, start_time, stop_time, tenant_id)   # 获取整体的数据
    for i in range(0, len(usage_info["tenant_usages"])):
        tenant_usage_data = copy.deepcopy(usage_info["tenant_usages"][i])  # 深度复制出单个用户统计数据
        project_id = usage_info["tenant_usages"][i]["tenant_id"]
        tenant_name = get_tenant_name_by_tenant_id(token_id, project_id)  # 根据项目id获取项目的名字
        tenant_usage_data["tenant_name"] = tenant_name
        tenant_usage_data.pop("server_usages")  # 除去单租户数据中的“server_usages”字段
        single_tenant_data = {}  # 用于统计mb、vcpus、local_gb的值
        memory_mb = 0
        vcpus = 0
        local_gb = 0
        tenant_servers_info = usage_info["tenant_usages"][i]["server_usages"]  # 单个租户下所有虚拟机信息
        for j in range(0, len(tenant_servers_info)):  # 统计虚拟内核、磁盘、内存
            if tenant_servers_info[j]["state"] != "terminated":  # 除去状态为terminated虚拟机
                memory_mb = memory_mb + tenant_servers_info[j]["memory_mb"]
                vcpus = vcpus + tenant_servers_info[j]["vcpus"]
                local_gb = local_gb + tenant_servers_info[j]["local_gb"]
        single_tenant_data["memory_mb"] = memory_mb
        single_tenant_data["vcpus"] = vcpus
        single_tenant_data["local_gb"] = local_gb
        single_tenant_tmp = dict(single_tenant_data, ** tenant_usage_data)  # 用于合并usage数据和统计数据
        tenants_usage_info["tenant_usages"].append(single_tenant_tmp)
    return tenants_usage_info


def get_num_info(admin_token_id, admin_tenant_id):
    """获取租户、物理主机、虚拟主机、网络、子网、路由器个数"""
    num_info = []
    user_num = len(get_users_list(admin_token_id)["users"])  # 获取用户数量
    user_num_info = {}
    user_num_info["name"] = "user_num"
    user_num_info["number"] = user_num
    num_info.append(user_num_info)
    physical_num = len(get_hypervisor_detail(admin_token_id, admin_tenant_id)["hypervisors"])  # 获取物理机的个数
    physical_num_info = {}
    physical_num_info["name"] = "physical_num"
    physical_num_info["number"] = physical_num
    num_info.append(physical_num_info)
    server_num = len(get_all_tenant_instances(admin_token_id, admin_tenant_id)["servers"])  # 获取总的虚拟机个数
    server_num_info = {}
    server_num_info["name"] = "server_num"
    server_num_info["number"] = server_num
    num_info.append(server_num_info)
    network_num = len(get_all_networks(admin_token_id)["networks"])  # 获取网络个数
    network_num_info = {}
    network_num_info["name"] = "network_num"
    network_num_info["number"] = network_num
    num_info.append(network_num_info)
    subnet_num = len(get_tenant_subnets(admin_token_id)["subnets"])  # 获取子网个数
    subnet_num_info = {}
    subnet_num_info["name"] = "subnet_num"
    subnet_num_info["number"] = subnet_num
    num_info.append(subnet_num_info)
    router_num = len(get_tenant_routers(admin_token_id)["routers"])  # 获取路由器个数
    router_num_info = {}
    router_num_info["name"] = "router_num"
    router_num_info["number"] = router_num
    num_info.append(router_num_info)
    return num_info


def get_abstarct_info(token_id, start_time, stop_time, tenant_id):
    """获取整个云平台下的摘要信息"""
    tenant_usage = get_tenant_usage(token_id, start_time, stop_time, tenant_id)  # 获取资源使用情况信息
    num_info = get_num_info(token_id, tenant_id)
    tenant_usage["num_info"] = num_info
    return tenant_usage





