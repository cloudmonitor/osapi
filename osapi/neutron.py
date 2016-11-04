# _*_ coding:utf-8 _*_


import copy


from settings import *


def get_tenant_networks(token_id):
    """获取租户的network"""
    network_info = get_all_networks(token_id)
    tenant_networks = {"networks": []}
    for i in range(len(network_info['networks'])):
        if not network_info['networks'][i]["router:external"]:
            tenant_networks["networks"].append(network_info['networks'][i])
    return tenant_networks


def get_all_networks(token_id):
    """获得所有的网络"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT
    r = requests.get(url+'/networks', headers=headers)
    return r.json()


def get_one_network(token_id, network_id):
    """获得某一网络的信息"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT+'/networks/' + network_id
    r = requests.get(url, headers=headers)
    return r.json()


def get_tenant_subnets(token_id):
    """获取租户的子网"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT
    r = requests.get(url+'/subnets', headers=headers)
    return r.json()


def get_tenant_routers(token_id):
    """获取租户的路由"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT
    r = requests.get(url+'/routers', headers=headers)
    return r.json()


def get_one_router(token_id, router_id):
    """获取某一路由器的信息"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT+'/routers/' + router_id
    r = requests.get(url, headers=headers)
    return r.json()


def get_tenant_ports(token_id):
    """ 获取所有的端口的信息"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + "/ports"
    r = requests.get(url=url, headers=headers)
    return r.json()


# def get_new_subnets(token_id):
#     """获取有ip地址池的子网"""
#     subnet_info = []
#     subnet = {}
#     headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NEUTRON_ENDPOINT
#     r = requests.get(url+'/subnets', headers=headers)
#     subnet_test = r.json()
#     for i in range(len(subnet_test['subnets'])):
#         if subnet_test['subnets'][i]['allocation_pools']:
#             subnet_info.append(subnet_test['subnets'][i])
#     subnet['subnets'] = subnet_info
#     return subnet


def get_router_ports(token_id, router_id):
    """获取路由器相关的port"""
    router_port={}
    router_port_info = []
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + "/ports"
    port_data = requests.get(url=url, headers=headers).json()
    for i in range(len(port_data['ports'])):
        if port_data['ports'][i]['device_id'] == router_id:
            router_port_info.append(port_data['ports'][i])
    router_port['ports'] = router_port_info
    return router_port


def create_network(token_id, data):
    """创建网络"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    network_url = NEUTRON_ENDPOINT + "/networks"
    data = json.loads(data)
    print json.dumps(data)
    network_data = json.dumps(data[0])
    print network_data
    r = requests.post(url=network_url, data=network_data, headers=headers)
    return_info = r.json()
    print json.dumps(return_info)
    if len(data) == 2:
        subnet_data = data[1]
        subnet_data['subnet']['network_id'] = return_info['network']['id']
        subnet_data =json.dumps(subnet_data)
        url = NEUTRON_ENDPOINT + "/subnets"
        print subnet_data
        subnet_info = requests.post(url=url, data=subnet_data, headers=headers)
        return_info = subnet_info.json()
    return return_info


def update_network(token_id, data, network_id):
    """更新网络"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + "/networks/" + network_id
    print url
    r = requests.put(url=url, data=data, headers=headers)
    return r.json()


def delete_network(token_id, network_id_list):
    """删除网络"""
    delete_status = {}
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    for i in range(len(network_id_list["network_ids"])):
        url = NEUTRON_ENDPOINT + '/networks/' + network_id_list["network_ids"][i]
        r = requests.delete(url=url, headers=headers)
        delete_status[network_id_list["network_ids"][i]] = r.status_code
    return delete_status


def create_subnet(token_id, data):
    """创建一个子网"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + "/subnets"
    r = requests.post(url=url, data=data, headers=headers)
    return r.json()


def update_subnet(token_id, data, subnet_id):
    """更新子网"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + "/subnets/" + subnet_id
    print url
    r = requests.put(url=url, data=data, headers=headers)
    return r.json()


def delete_subnet(token_id, subnet_id_list):
    """删除子网"""
    delete_status = {}
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    for i in range(len(subnet_id_list["subnet_ids"])):
        url = NEUTRON_ENDPOINT + '/subnets/' + subnet_id_list["subnet_ids"][i]
        print url
        r = requests.delete(url=url, headers=headers)
        if r.status_code == 204:
            delete_status[subnet_id_list["subnet_ids"][i]] = r.status_code
        else:
            delete_status[subnet_id_list["subnet_ids"][i]] = r.json()
    return delete_status


def create_port(token_id, data):
    """创建一个端口"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + "/ports"
    r = requests.post(url=url, data=data, headers=headers)
    return r.json()


def update_port(token_id,data,port_id):
    """更新端口"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + "/ports/" + port_id
    print url
    r = requests.put(url=url, data=data, headers=headers)
    return r.json()


def delete_port(token_id, port_id_list):
    """删除端口"""
    delete_status = {}
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    for i in range(len(port_id_list["port_ids"])):
        url = NEUTRON_ENDPOINT + '/ports/' + port_id_list["port_ids"][i]
        r = requests.delete(url=url, headers=headers)
        delete_status[port_id_list["port_ids"][i]] = r.status_code
    return delete_status


def create_router(token_id, data):
    """创建一个路由"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + "/routers"
    r = requests.post(url=url, data=data, headers=headers)
    return r.json()


def update_router(token_id, data, router_id):
    """更新路由"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + "/routers/" + router_id
    print url
    r = requests.put(url=url, data=data, headers=headers)
    return r.json()


def delete_router(token_id, router_id_list):
    """删除路由"""
    delete_status = {}
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    for i in range(len(router_id_list["router_ids"])):
        url = NEUTRON_ENDPOINT + '/routers/' + router_id_list["router_ids"][i]
        r = requests.delete(url=url, headers=headers)
        delete_status[router_id_list["router_ids"][i]] = r.status_code
    return delete_status


def get_route_table(token_id, router_id):
    """获取某一路由的路由表"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + '/routers/' + router_id
    r = requests.get(url=url, headers=headers)
    router_info = r.json()
    router_table = router_info['router']['routes']
    return router_table


def disconnect_subnet(token_id):
    """没有关联到路由器的子网"""
    port_info = get_tenant_ports(token_id)
    subnet_info = get_tenant_subnets(token_id)
    subnet_info_return = copy.deepcopy(subnet_info)
    for i in range(len(port_info['ports'])):
        if port_info['ports'][i]['device_owner'] == "network:router_interface":
            for j in range(len(subnet_info['subnets'])):
                if subnet_info['subnets'][j]['id'] == port_info['ports'][i]['fixed_ips'][0]['subnet_id']:
                    subnet_info_return['subnets'].remove(subnet_info['subnets'][j])
    return subnet_info_return


def add_router_interface(token_id, router_id, data):
    """给路由器增加端口"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + "/routers/" + router_id + "/add_router_interface"
    r = requests.put(url=url, data=data, headers=headers)
    return r.json()


def remove_router_interface(token_id, router_id, data):
    """路由器删除端口"""
    delete_status = []
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + "/routers/" + router_id + "/remove_router_interface"
    data = json.loads(data)
    for i in range(len(data['router_ports'])):
        subnet_id_info = data['router_ports'][i]
        r = requests.put(url=url, data=json.dumps(subnet_id_info), headers=headers)
        print r.json()
        delete_status.append(r.status_code)
    return delete_status


def get_tenant_ext_net(token_id):
    """获取租户的外网数据"""
    extnet_info = {"ext_net": []}
    network_info = get_all_networks(token_id)
    for i in range(len(network_info['networks'])):
        if network_info['networks'][i]['router:external']:
            extnet_info["ext_net"].append(network_info['networks'][i])
    return extnet_info


def get_dis_port(token_id):
    """获取无关的端口"""
    port_info = get_tenant_ports(token_id)
    delete_port_list_info = []
    delete_port_list = {}
    for i in range(len(port_info["ports"])):
        if not port_info['ports'][i]['device_owner']:
            delete_port_list_info.append(port_info['ports'][i]['id'])
    delete_port_list['port_ids'] = delete_port_list_info
    return  delete_port_list


def get_subnet_servers(token_id, tenant_id, subnet_id):
    """获取某一子网下包括虚拟机"""
    from nova import get_tenant_instances
    subnet_vm_list_info = []
    subnet_vm_list = {}
    subnet_port_list_info = []
    subnet_port_list = {}
    port_info = get_tenant_ports(token_id)
    servers_info = get_tenant_instances(token_id, tenant_id)
    for i in range(len(port_info['ports'])):
        if port_info['ports'][i]['device_owner'].startswith('compute:compute') and port_info['ports'][i]['fixed_ips'][0]['subnet_id'] == subnet_id:
            subnet_port_list_info.append(port_info['ports'][i])
    subnet_port_list['ports'] = subnet_port_list_info
    for j in range(len(subnet_port_list['ports'])):
        for k in range(len(servers_info['servers'])):
            if subnet_port_list['ports'][j]['device_id'] == servers_info['servers'][k]['id']:
                subnet_vm_list_info.append(servers_info['servers'][k]['id'])
    subnet_vm_list['servers'] = subnet_vm_list_info
    return subnet_vm_list


def get_server_port(token_id, tenant_id):
    """获取虚拟机的端口信息"""
    ports_info_list = []
    port_infos = {}
    from nova import get_tenant_instances
    ports_info = get_tenant_ports(token_id)
    servers_info = get_tenant_instances(token_id, tenant_id)
    subnet_info = get_tenant_subnets(token_id)
    for i in range(len(ports_info['ports'])):
        if ports_info['ports'][i]['device_owner'].startswith('compute') or not ports_info['ports'][i]['device_owner']:
            for j in range(len(subnet_info['subnets'])):
                if ports_info['ports'][i]['fixed_ips'][0]['subnet_id'] == subnet_info['subnets'][j]['id']:
                    ports_info['ports'][i]['fixed_ips'][0]['subnet_name'] = subnet_info['subnets'][j]['name']
            for k in range(len(servers_info['servers'])):
                if ports_info['ports'][i]['device_id'] == servers_info['servers'][k]['id']:
                    ports_info['ports'][i]['device_name'] = servers_info['servers'][k]['name']
                    servers_address = servers_info['servers'][k]['addresses'].values()
                    for s in range(len(servers_address[0])):
                        if servers_address[0][s]['OS-EXT-IPS:type'] == 'floating':
                            ports_info['ports'][i]['floating_ip'] = servers_address[0][s]['addr']
            ports_info_list.append(ports_info['ports'][i])
    port_infos['ports'] = ports_info_list
    return port_infos



