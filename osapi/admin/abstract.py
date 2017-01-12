# _*_ coding:utf-8 _*_


from osapi.settings import *


def get_tenant_usage(token_id, start_time, stop_time, tenant_id):
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


