# _*_ coding:utf-8 _*_


from osapi.settings import *


def get_physical_usage(token_id, tenant_id):
    """获取物理主机的使用情况"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id)
    r = requests.get(url=url + "/os-hypervisors/detail", headers=headers)
    hypervisors_usage = {}
    hypervisors_usage["hypervisors"] = []  # 用于存储最后的值
    physical_info = r.json()
    hypervisors_info = physical_info["hypervisors"]
    for i in range(0, len(hypervisors_info)):
        physical_tmp = {}  # 临时存储physical信息的变量
        physical_tmp["vcpus_used"] = physical_info["hypervisors"][i]["vcpus_used"]
        physical_tmp["local_gb_used"] = physical_info["hypervisors"][i]["local_gb_used"]
        physical_tmp["memory_mb_used"] = physical_info["hypervisors"][i]["memory_mb_used"]
        physical_tmp["vcpus"] = physical_info["hypervisors"][i]["vcpus"]
        physical_tmp["hypervisor_hostname"] = physical_info["hypervisors"][i]["hypervisor_hostname"]
        physical_tmp["memory_mb"] = physical_info["hypervisors"][i]["memory_mb"]
        physical_tmp["local_gb"] = physical_info["hypervisors"][i]["local_gb"]
        hypervisors_usage["hypervisors"].append(physical_tmp)
    return hypervisors_usage


def get_statistics_info(token_id, tenant_id):
    """获取云平台下总的统计信息（未分节点）"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id)
    r = requests.get(url=url + "/os-hypervisors/statistics", headers=headers)
    return r.json()