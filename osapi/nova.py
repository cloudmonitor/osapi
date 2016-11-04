# _*_ coding:utf-8 _*_

from settings import *
from images import get_tenant_images


def get_tenant_instances_image(token_id, tenant_id):
    """获取某一租户下的所有vm,并将镜像的名字加入到了虚拟机的内容中"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id)
    r = requests.get(url+'/servers/detail', headers=headers)
    instances_info = r.json()
    images_info = get_tenant_images(token_id)
    for i in range(len(instances_info['servers'])):
        image_id = instances_info['servers'][i]['image']['id']
        for j in range(len(images_info['images'])):
            if image_id == images_info['images'][j]['id']:
                instances_info['servers'][i]['image']['image_name'] = images_info['images'][j]['name']
                break
    return instances_info


def get_tenant_instances(token_id, tenant_id):
    """获取某一租户下所有的VM"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id)
    r = requests.get(url+'/servers/detail', headers=headers)
    return r.json()


def get_tenant_instance(token_id, tenant_id, instance_id):
    """获取某一租户下的某一vm"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id)
    r = requests.get(url+'/servers/'+instance_id, headers=headers)
    return r.json()


def get_tenant_sg(token_id, tenant_id):
    """获取租户的安全组"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id)
    r = requests.get(url+'/os-security-groups', headers=headers)
    return r.json()


def get_tenant_flavors(token_id, tenant_id):
    """获取租户的类型"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id)
    r = requests.get(url+'/flavors/detail', headers=headers)
    return r.json()


def get_tenant_os_availability_zone(token_id,tenant_id):
    """获取可分配的域"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/os-availability-zone"
    r = requests.get(url=url, headers=headers)
    return r.json()


def get_server_interface(token_id, tenant_id, servers_id):
    """获取某一虚拟机的interface信息"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/servers/" + servers_id + "/os-interface"
    r = requests.get(url=url, headers=headers)
    return r.json()


def create_servers(token_id, tenant_id, data):
    """创建一个虚拟机"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/servers"
    r = requests.post(url=url, data=data, headers=headers)
    return r.json()


def update_servers(token_id, tenant_id, data, servers_id):
    """更新虚拟机 编辑云主机在这里里面"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/servers/" + servers_id
    r = requests.put(url=url, data=data, headers=headers)
    return r.json()


def delete_servers(token_id, tenant_id, servers_id_list):
    """终止虚拟机"""
    delete_status = {}
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    for i in range(len(servers_id_list["servers_ids"])):
        url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/servers/" + servers_id_list["servers_ids"][i]
        r = requests.delete(url=url, headers=headers)
        delete_status[servers_id_list["servers_ids"][i]] = r.status_code
    return delete_status


def bind_interface(token_id, tenant_id, data, servers_id):
    """创建网卡在绑定到虚拟机"""
    from neutron import create_port
    print data
    network_id = data['interface']["network_id"]
    subnet_id = data['interface']["subnet_id"]
    port_data = '{"port": {"network_id": "%s","fixed_ips": [{"subnet_id": "%s"}]}}' % (network_id, subnet_id)
    port_r = create_port(token_id, port_data)
    port_id = port_r['port']['id']
    data = '{"interfaceAttachment": {"port_id": "%s"}}' %(port_id)
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/servers/" + servers_id + "/os-interface"
    r = requests.post(url=url, data=data, headers=headers)
    return r.json()


def touch_interface(token_id, tenant_id, data, servers_id):
    """已经存在网卡绑定到虚拟机"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/servers/" + servers_id + "/os-interface"
    r = requests.post(url=url,data=json.dumps(data), headers=headers)
    return r.json()


def detach_interface(token_id, tenant_id, servers_id, port_id):
    """解绑虚拟机上的接口"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/servers/" + servers_id + "/os-interface/" + port_id
    r = requests.delete(url=url, headers=headers)
    return r.status_code


def detach_interface_list(token_id, tenant_id, servers_id, data):
    result_list_info = []
    result_list = {}
    for i in range(len(data['ports_id'])):
        port_id = data['ports_id'][i]
        result_list_info.append(detach_interface(token_id, tenant_id, servers_id, port_id))
    result_list['del_status'] = result_list_info
    return result_list


def delete_interface(token_id, tenant_id, servers_id,inter_data):
    """解绑虚拟网卡"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    ip_address = inter_data['ip_address']
    print ip_address
    port_data = get_server_interface(token_id, tenant_id, servers_id)
    print port_data
    for i in range(len(port_data['interfaceAttachments'])):
        if ip_address == port_data['interfaceAttachments'][i]['fixed_ips'][0]['ip_address']:
            port_id = port_data['interfaceAttachments'][i]['port_id']
            print port_id
            url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/servers/" + servers_id + "/os-interface/" + port_id
            r = requests.delete(url=url, headers=headers)
            break
    return r.status_code


def create3_servers(token_id, tenant_id, servers_data):
    """循环创建虚拟机"""
    status_list = []
    servers_data = json.loads(servers_data)
    max_count = servers_data['server'].pop('max_count')
    servers_data = json.dumps(servers_data)
    for i in range(int(max_count)):
        server_r = create2_servers(token_id, tenant_id, servers_data)
        status_list.append(server_r)
    return status_list


def create2_servers(token_id, tenant_id, servers_data):
    """创建指定子网的虚拟机"""
    from neutron import create_port
    servers_data = json.loads(servers_data)
    network_info = servers_data['server'].pop('network_info')
    for i in range(len(network_info)):
        network_id = network_info[i]["network_id"]
        subnet_id = network_info[i]["subnet_id"]
        port_data = '{"port": {"network_id": "%s","fixed_ips": [{"subnet_id": "%s"}]}}' % (network_id, subnet_id)
        print port_data
        port_r = create_port(token_id, port_data)
        print port_r
        port_id = port_r['port']['id']
        for j in range(len(servers_data['server']['networks'])):
            if network_id == servers_data['server']['networks'][j]['uuid']:
                servers_data['server']['networks'][j]['port'] = port_id
    print servers_data
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/servers"
    server_r = requests.post(url=url, data=json.dumps(servers_data), headers=headers)
    # server_r = server_r.status_code
    server_r = server_r.json()
    return server_r


def server_security_group(token_id, tenant_id, server_id):
    """获取虚拟机的安全组"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/servers/" + server_id + "/os-security-groups"
    print url
    r = requests.get(url=url,headers=headers)
    return r.json()


def disserver_security_group(token_id, tenant_id, server_id):
    """获取虚拟机没有的的安全组"""
    dis_instance_sg_info = []
    dis_instance_sg = {}
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/servers/" + server_id + "/os-security-groups"
    print url
    r = requests.get(url=url, headers=headers)
    server_sg = r.json()
    print server_sg
    instance_sg = get_tenant_sg(token_id, tenant_id)
    for i in range(len(instance_sg['security_groups'])):
        flag = True
        for j in range(len(server_sg['security_groups'])):
            if instance_sg['security_groups'][i]['id'] == server_sg['security_groups'][j]['id']:
                flag = False
        if flag:
            dis_instance_sg_info.append(instance_sg['security_groups'][i])
    dis_instance_sg['security_groups'] = dis_instance_sg_info
    return dis_instance_sg


def bind_security_group(token_id, tenant_id, data, servers_id):
    """绑定安全组"""
    bind_status_list =[]
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/servers/" + servers_id + "/action"
    data = json.loads(data)
    for i in range(len(data['addSecurityGroup'])):
        bind_data = '{"addSecurityGroup": {"name": "%s"}}' % (data['addSecurityGroup'][i])
        r = requests.post(url=url, data=bind_data, headers=headers)
        bind_status_list.append(r.status_code)
    return bind_status_list


def remove_security_group(token_id, tenant_id, data, servers_id):
    """解绑安全组"""
    remove_status_list =[]
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/servers/" + servers_id + "/action"
    print url
    data = json.loads(data)
    for i in range(len(data['removeSecurityGroup'])):
        remove_data = '{"removeSecurityGroup": {"name": "%s"}}' % (data['removeSecurityGroup'][i])
        r = requests.post(url=url, data=remove_data, headers=headers)
        remove_status_list.append(r.status_code)
    return remove_status_list


def server_update_sg(token_id,tenant_id,server_id,data):
    """虚拟机更新安全组"""
    add_sg_data = {}
    add_sg_data_info =[]
    remove_sg_data = {}
    remove_sg_data_info =[]
    server_sg = server_security_group(token_id, tenant_id, server_id)
    sg_data = data
    print json.dumps(sg_data)
    for i in range(len(sg_data['security_groups'])):
        flag = True
        for j in range(len(server_sg['security_groups'])):
            if sg_data['security_groups'] == server_sg['security_groups'][j]['name']:
                flag = False
        if flag:
            add_sg_data_info.append(sg_data['security_groups'][i])
    add_sg_data['addSecurityGroup'] = add_sg_data_info
    print json.dumps(add_sg_data)
    bind_status_list = bind_security_group(token_id, tenant_id, json.dumps(add_sg_data), server_id)
    for i in range(len(server_sg['security_groups'])):
        flag = True
        for j in range(len(sg_data['security_groups'])):
            if sg_data['security_groups'][j] == server_sg['security_groups'][i]['name']:
                flag = False
        if flag:
            remove_sg_data_info.append(server_sg['security_groups'][i]['name'])
    remove_sg_data['removeSecurityGroup'] = remove_sg_data_info
    print json.dumps(remove_sg_data)
    remove_status_list = remove_security_group(token_id, tenant_id, json.dumps(remove_sg_data), server_id)
    bind_status_list.extend(remove_status_list)
    return bind_status_list


def action_server(token_id, tenant_id, servers_id, data):
    """对于虚拟机的、floatingips、中止虚拟机、暂停之后的恢复虚拟机、挂起、挂起恢复、\
    锁定和解锁虚拟机、硬重启、软重启、关闭虚拟机、重建虚拟机、启动虚拟机"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/servers/" + servers_id + "/action"
    print url
    r = requests.post(url=url, data=data, headers=headers)
    print r.status_code


def get_server_console(token_id, tenant_id, servers_id, data):
    """获取虚拟机远程登录"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/servers/" + servers_id + "/action"
    print url
    r = requests.post(url=url, data=data, headers=headers)
    return r.json()