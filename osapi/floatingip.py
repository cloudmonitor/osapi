# _*_ coding:utf-8 _*_

from settings import *
from neutron import get_tenant_ports


def get_floating_ips(token_id):
    """ 列出floating ip"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + '/floatingips'
    r = requests.get(url, headers=headers)
    return r.json()


def get_disallocate_floating_ips(token_id):
    """ 列出未分配的floating ip"""
    floating_ips_info = get_floating_ips(token_id)
    floating_ips = []
    float_ips = {}
    for i in range(len(floating_ips_info['floatingips'])):
        print len(floating_ips_info['floatingips'])
        if floating_ips_info['floatingips'][i]['status'] == 'DOWN':
            floating_ips.append(floating_ips_info['floatingips'][i])
    float_ips['floatingips'] = floating_ips
    return float_ips


def get_floating_ips_pool(token_id, tenant_id):
    """获取分配外网IP的网络"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + '/os-floating-ip-pools'
    r = requests.get(url, headers=headers)
    return r.json()


def allocate_floating_ips(token_id, data):
    """分配一个floating ip"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + '/floatingips'
    r = requests.post(url, data=data, headers=headers)
    return r.json()


def release_floating_ips(token_id, floating_ip_ids):
    """分配一个floating ip"""
    release_status = {}
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    for i in range(len(floating_ip_ids["floating_ip_ids"])):
        url = NEUTRON_ENDPOINT + '/floatingips/' + floating_ip_ids["floating_ip_ids"][i]
        r = requests.delete(url, headers=headers)
        release_status[floating_ip_ids["floating_ip_ids"][i]] = r.status_code
    return release_status


def associate_floatingip_prot(token_id, floatingip_id, data):
    """关联浮动IP到指定端口"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + "/floatingips/" + floatingip_id
    r = requests.put(url, data=data, headers=headers)
    return r.json()


def get_disassociate_floatingip_port(token_id):
    """获得未被关联的虚拟机端口"""
    ports = get_tenant_ports(token_id)
    floatingips = get_floating_ips(token_id)
    disassociate_port = {"disassociate_port": []}
    for i in range(len(ports["ports"])):
        if ports["ports"][i]["device_owner"].startswith("compute:"):
            disassociate_port["disassociate_port"].append(ports["ports"][i])
            for j in range(len(floatingips["floatingips"])):
                if ports["ports"][i]["id"] == floatingips["floatingips"][j]["port_id"]:
                    disassociate_port["disassociate_port"].remove(ports["ports"][i])
    return disassociate_port



