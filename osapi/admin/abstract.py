# _*_ coding:utf-8 _*_


from osapi.settings import *
from osapi.user import *
from osapi.nova import *
from osapi.neutron import *


def get_tenant_usage(token_id, start_time, stop_time, tenant_id ):
    """获取租户的虚拟内核、磁盘、内存以及相应的使用时间"""
    tenants_usage_info = {}  # 用于返回的数据
    tenants_usage_info["tenant_usages"] = []
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id)
    r = requests.get(url=url + "/os-simple-tenant-usage?detailed=1&start=" + start_time + "&end="+stop_time, headers=headers)
    usage_info = r.json()   # 获取整体的数据
    # print json.dumps(usage_info)
    tenant_usage = usage_info["tenant_usages"]  # 处理数据，从server_usages里面统计出租户的虚拟内核、磁盘、内存
    for i in range(0, len(tenant_usage)):
        tenant_single_info = {}
        # print type(tenant_usage)
        tenant_usage_single = tenant_usage[i]  # 将单个租户的信息赋值给tenant_usage_single
        tenant_single_info["total_memory_mb_usage"] = tenant_usage_single["total_memory_mb_usage"]
        tenant_single_info["total_vcpus_usage"] = tenant_usage_single["total_vcpus_usage"]
        tenant_single_info["start"] = tenant_usage_single["start"]
        tenant_single_info["stop"] = tenant_usage_single["stop"]
        tenant_single_info["tenant_id"] = tenant_usage_single["tenant_id"]
        tenant_single_info["total_hours"] = tenant_usage_single["total_hours"]
        tenant_single_info["total_local_gb_usage"] = tenant_usage_single["total_local_gb_usage"]
        for j in range(0,len(tenant_usage_single["server_usages"])):  # 统计虚拟内核、磁盘、内存
            memory_mb = 0
            vcpus = 0
            local_gb = 0
            memory_mb = memory_mb + tenant_usage_single["server_usages"][j]["memory_mb"]
            vcpus = vcpus + tenant_usage_single["server_usages"][j]["vcpus"]
            local_gb = local_gb + tenant_usage_single["server_usages"][j]["local_gb"]
        tenant_single_info["memory_mb"] = memory_mb
        tenant_single_info["vcpus"] = vcpus
        tenant_single_info["local_gb"] = local_gb
        tenants_usage_info["tenant_usages"].append(tenant_single_info)
    return tenants_usage_info


def get_num_info(admin_token_id):
    """获取租户、物理主机、虚拟主机、网络、子网、路由器个数"""
    num_info = []
    user_num = len(get_users_list(admin_token_id)["users"])  # 获取用户数量
    user_num_info = {}
    user_num_info["user_num"] = user_num
    num_info.append(user_num_info)
    physical_num = len(get_hypervisor_detail()["hypervisors"])  # 获取物理机的个数
    physical_num_info = {}
    physical_num_info["physical_num"] = physical_num
    num_info.append(physical_num_info)
    server_num = len(get_all_tenant_instances()["servers"])  # 获取总的虚拟机个数
    server_num_info = {}
    server_num_info["server_num"] = server_num
    num_info.append(server_num_info)
    network_num = len(get_all_networks(admin_token_id)["networks"])  # 获取网络个数
    network_num_info = {}
    network_num_info["network_num"] = network_num
    num_info.append(network_num_info)
    subnet_num = len(get_tenant_subnets(admin_token_id))  # 获取子网个数
    subnet_num_info = {}
    subnet_num_info["subnet_num"] = subnet_num
    num_info.append(subnet_num_info)
    router_num = len(get_tenant_routers(admin_token_id))  # 获取路由器个数
    router_num_info = {}
    router_num_info["router_num"] = router_num
    num_info.append(router_num_info)
    return num_info


def get_abstarct_info(token_id, start_time, stop_time, tenant_id):
    """获取整个云平台下的摘要信息"""
    tenant_usage = get_tenant_usage(token_id, start_time, stop_time, tenant_id)  # 获取资源使用情况信息
    num_info = get_num_info(token_id)
    tenant_usage["num_info"] = num_info
    return tenant_usage





