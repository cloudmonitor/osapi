# _*_ coding:utf-8 _*_

from neutron import get_all_networks, get_tenant_subnets, get_tenant_routers, get_tenant_ports, get_tenant_networks, \
    get_one_network, get_one_router
from nova import get_tenant_instances,get_tenant_instance
from settings import *

SERVER_NUM = 0
NET_NUM = 0
ROUTER_NUM = 0
EXNET_NUM = 0
SUB_NUM = 0
CANVAS_X =700
CANVAS_Y =700


def _get_tuopu_port_info(token_id, tenant_id):
    """获取拓扑的端口信息 srcDeviceId是子网id,dstDeviceId是device_id,"""
    ports_list = []
    all_port_info = get_tenant_ports(token_id)
    for i in range(len(all_port_info['ports'])):
        port_info = {}
        if not all_port_info['ports'][i]['device_id'].startswith('dhcp') and not all_port_info['ports'][i]['device_owner'].startswith("network:router_interface") and all_port_info['ports'][i]['device_owner']:
            """子网与虚拟机的连线"""
            port_info["status"] = all_port_info['ports'][i]['status']
            port_info["srcDeviceId"] = all_port_info['ports'][i]['fixed_ips'][0]['subnet_id']
            port_info["url"] = ""
            port_info["device_owner"] = all_port_info['ports'][i]["device_owner"]
            port_info["fixed_ips"] = all_port_info['ports'][i]["fixed_ips"]
            port_info["id"] = all_port_info['ports'][i]["id"]
            port_info["dstDeviceId"] = all_port_info['ports'][i]["device_id"]
            port_info["stroke"] = "black"
            port_info["strokeWidth"] = 2
            port_info["is_del"] = "True"
            ports_list.append(port_info)
    all_routers_info = get_tenant_routers(token_id)
    for i in range(len(all_routers_info["routers"])):
        if all_routers_info['routers'][i]["external_gateway_info"]:
            """路由器与外网连线"""
            ex_port_info = {}
            if get_router_servers(token_id, tenant_id, all_routers_info['routers'][i]['id']):
                ex_port_info["is_del"] = "True"
            else:
                ex_port_info["is_del"] = "False"
            ex_port_info["srcDeviceId"] = all_routers_info['routers'][i]["external_gateway_info"]["network_id"]
            ex_port_info["fixed_ips"] = all_routers_info['routers'][i]["external_gateway_info"]["external_fixed_ips"]
            ex_port_info["id"] = "gateway"+all_routers_info['routers'][i]["external_gateway_info"]["network_id"]
            ex_port_info["dstDeviceId"] = all_routers_info['routers'][i]["id"]
            ex_port_info["stroke"] = "#00CD00"
            ex_port_info["strokeWidth"] = 2
            ports_list.append(ex_port_info)
    return ports_list


def router_network(token_id, tenant_id):
    """网络与路由器连线"""
    all_port_info = get_tenant_ports(token_id)
    network_router_id_info = []
    ports_list = []
    all_routers_info = get_tenant_routers(token_id)
    for i in range(len(all_port_info['ports'])):
        port_info ={}
        fixed_ips = []
        if all_port_info['ports'][i]['device_owner'].startswith("network:router_interface"):
            if (all_port_info['ports'][i]['network_id'], all_port_info['ports'][i]['device_id']) not in network_router_id_info:
                network_router_id_info.append((all_port_info['ports'][i]['network_id'], all_port_info['ports'][i]['device_id']))
                if get_router_servers(token_id, tenant_id, all_port_info['ports'][i]['device_id']):
                    port_info["is_del"] = "False"
                else:
                    port_info["is_del"] = "True"
                port_info["status"] = all_port_info['ports'][i]['status']
                port_info["srcDeviceId"] = all_port_info['ports'][i]['network_id']
                port_info["url"] = ""
                port_info["device_owner"] = all_port_info['ports'][i]["device_owner"]
                fixed_ips.append(all_port_info['ports'][i]["fixed_ips"][0])
                port_info["fixed_ips"] = fixed_ips
                port_info["id"] = all_port_info['ports'][i]["id"]
                port_info["dstDeviceId"] = all_port_info['ports'][i]["device_id"]
                port_info["stroke"] = "#00CD00"
                port_info["strokeWidth"] = 2
                ports_list.append(port_info)
            else:
                index = network_router_id_info.index((all_port_info['ports'][i]['network_id'], all_port_info['ports'][i]['device_id']))
                # network_router_id_info.insert(index, all_port_info['ports'][i]['network_id'])
                ports_list[index]["fixed_ips"].append(all_port_info['ports'][i]["fixed_ips"][0])
    return ports_list


def network_subnet(token_id):
    """获取网络与子网的关系图srcDeviceId是网络id,dstDeviceId是subnet_id"""
    line_list = []
    network_info = get_tenant_networks(token_id)
    port_info = get_tenant_ports(token_id)
    for i in range(len(network_info['networks'])):
        line_info = {}
        for j in range(len(network_info['networks'][i]['subnets'])):
            line_info['srcDeviceId'] = network_info['networks'][i]['id']
            line_info['dstDeviceId'] = network_info['networks'][i]['subnets'][j]
            line_info["strokeWidth"] = 2
            line_info["is_del"] = "False"
            for k in range(len(port_info['ports'])):
                if port_info['ports'][k]['device_owner'].startswith("network:router_interface") and network_info['networks'][i]['subnets'][j] == port_info['ports'][k]['fixed_ips'][0]['subnet_id']:
                    line_info["stroke"] = "#00CD00"
                    break
                else:
                    line_info["stroke"] = "black"
            line_list.append(line_info)
            line_info = {}
    return line_list


def get_network_servers(token_id, tenant_id, network_id):
    """获取某租户下某网络下的虚拟机"""
    network_info = get_one_network(token_id, network_id)
    servers_info = get_tenant_instances(token_id, tenant_id)
    network_servers_info = []
    for i in range(len(servers_info['servers'])):
        if not servers_info['servers'][i]['addresses']:
            continue
        if network_info['network']['name'] == servers_info['servers'][i]['addresses'].keys()[0]:
            network_servers_info.append(servers_info['servers'][i]['id'])
    return network_servers_info


def get_router_networks(token_id, router_id):
    """获取与路由器相关的网络信息"""
    router_network_id_info = []
    router_network = {}
    ports_info = get_tenant_ports(token_id)
    for i in range(len(ports_info['ports'])):
        if ports_info['ports'][i]['device_id'] == router_id:
            router_network_id_info.append(ports_info['ports'][i]['network_id'])
    router_network['networks_id'] = router_network_id_info
    return router_network


def get_router_servers(token_id, tenant_id, router_id):
    """获取路由器和相对应的虚拟机是否有floatingip 有返回True，没返回False"""
    router_network = get_router_networks(token_id, router_id)
    for i in range(len(router_network['networks_id'])):
        network_servers = get_network_servers(token_id, tenant_id, router_network['networks_id'][i])
        for j in range(len(network_servers)):
            instance_info = get_tenant_instance(token_id, tenant_id, network_servers[j])
            for k in range(len(instance_info['server']['addresses'].values()[0])):
                if instance_info['server']['addresses'].values()[0][k]['OS-EXT-IPS:type'] == "floating":
                    return False
    return True


def _get_tuopu_router_info(token_id):
    """ 获取路由器的tuopu信息 """
    routers_list = []
    all_routers_info = get_tenant_routers(token_id)
    for i in range(len(all_routers_info['routers'])):
        router_info = {}
        router_info["status"] = all_routers_info["routers"][i]["status"]
        router_info["external_gateway_info"] = all_routers_info["routers"][i]["external_gateway_info"]
        router_info["url"] = ""
        router_info["id"] = all_routers_info["routers"][i]["id"]
        router_info["name"] = all_routers_info["routers"][i]["name"]
        router_info["src"] = "./icon/device/router.png"
        router_info["device_name"] = "router"
        global ROUTER_NUM
        ROUTER_NUM += 1
        router_info["width"] = "%s" %(70)
        router_info["height"] = "%s" %(70)
        routers_list.append(router_info)
    return routers_list


def get_tuopu_subnet_info(token_id):
    """获取子网的拓扑信息"""
    subnet_info = []
    subnet_info_list = {}
    subnet_data = get_tenant_subnets(token_id)
    for i in range(len(subnet_data['subnets'])):
        subnet_info_list['network_id'] = subnet_data['subnets'][i]['network_id']
        subnet_info_list['name'] = subnet_data['subnets'][i]['name']
        subnet_info_list['id'] = subnet_data['subnets'][i]['id']
        subnet_info_list['cidr'] = subnet_data['subnets'][i]['cidr']
        subnet_info_list['src'] = "./icon/device/subnet.png"
        subnet_info_list['allocation_pools'] = subnet_data['subnets'][i]['allocation_pools']
        subnet_info_list["width"] = "%s" %(70)
        subnet_info_list["height"] = "%s" %(70)
        subnet_info_list["device_name"] = "subnet"
        global SUB_NUM
        SUB_NUM += 1
        subnet_info.append(subnet_info_list)
        subnet_info_list = {}
    return subnet_info


def _get_tuopu_network_info(network_info, subnet_info):
    """获取网络的路由信息"""
    net_info = []
    x = 360
    y = 360
    width = 100
    height = 100
    for i in range(len(network_info["networks"])):
        _net_info = {}
        _net_info["status"] = network_info["networks"][i]["status"]
        _net_info["subnets"] = _get_subnet_detail(network_info["networks"][i]["id"], subnet_info)
        _net_info["name"] = network_info["networks"][i]["name"]
        _net_info["router:external"] = network_info["networks"][i]["router:external"]
        _net_info["url"] = ""
        _net_info["id"] = network_info["networks"][i]["id"]
        if network_info["networks"][i]["router:external"]:
            _net_info["src"] = "./icon/device/extnet.png"
            _net_info["device_name"] = "ext_net"
            global EXNET_NUM
            EXNET_NUM +=1
        else:
             _net_info["src"] = "./icon/device/network.png"
             _net_info["device_name"] = "network"
             global NET_NUM
             NET_NUM  +=1
        # _net_info["x"] = "%s" %(x+i*width)
        # _net_info["y"] = "%s" %(y + i*height)
        _net_info["width"] = "%s" %(70)
        _net_info["height"] = "%s" %(70)
        net_info.append(_net_info)
    return net_info


def _get_tuopu_servers_info(severs_info_detail):
    servers_list = []
    x = 120
    y = 123
    width = 100
    height = 100
    for i in range(len(severs_info_detail["servers"])):
        one_servers_info = {}
        one_servers_info["status"] = severs_info_detail["servers"][i]["status"]
        one_servers_info["task"] = "null"
        one_servers_info["console"] = "vnc"
        one_servers_info["name"] = severs_info_detail["servers"][i]["name"]
        one_servers_info["url"] = ""
        one_servers_info["id"] = severs_info_detail["servers"][i]["id"]
        one_servers_info["src"] = "./icon/device/server.png"
        one_servers_info["device_name"] = "server"
        # one_servers_info["x"] = "%s" %(x+i*width)
        # one_servers_info["y"] = "%s" %(y + i*height)
        one_servers_info["width"] = "%s" %(70)
        one_servers_info["height"] = "%s" %(70)
        global SERVER_NUM
        SERVER_NUM += 1
        servers_list.append(one_servers_info)
    return servers_list


def _get_subnet_detail(network_id, subnet_info):
    simple_subnet_info = []
    for i in range(len(subnet_info["subnets"])):
        _simple_subnet_info = {}
        if subnet_info["subnets"][i]["network_id"] == network_id:
            _simple_subnet_info["url"] = ""
            _simple_subnet_info["cidr"] = subnet_info["subnets"][i]["cidr"]
            _simple_subnet_info["id"] = subnet_info["subnets"][i]["id"]
            simple_subnet_info.append(_simple_subnet_info)
    return simple_subnet_info


def get_network_topology(token_id, tenant_id):
    """这里是获取拓扑信息"""
    tuopu_info = {}
    tuopu_port = _get_tuopu_port_info(token_id, tenant_id)
    tuopu_net_subnet = network_subnet(token_id)
    tuopu_router = _get_tuopu_router_info(token_id)
    network_info = get_all_networks(token_id)
    subnet_info = get_tenant_subnets(token_id)
    tuopu_network = _get_tuopu_network_info(network_info, subnet_info)
    tuopu_subnet = get_tuopu_subnet_info(token_id)
    _servers_detail = get_tenant_instances(token_id, tenant_id)
    tuopu_server = _get_tuopu_servers_info(_servers_detail)
    router_network_info = router_network(token_id, tenant_id)
    tuopu_server += tuopu_router
    tuopu_server += tuopu_network
    tuopu_server += tuopu_subnet
    tuopu_port += tuopu_net_subnet
    tuopu_port += router_network_info
    tuopu_info['devices'] = tuopu_server
    tuopu_info['lines'] = tuopu_port
    return tuopu_info


def get_last_network_topology(token_id, tenant_id):
    global ROUTER_NUM, NET_NUM, EXNET_NUM, SERVER_NUM, CANVAS_X, CANVAS_Y, SUB_NUM
    tuopu_info = get_network_topology(token_id, tenant_id)
    max_num = max(ROUTER_NUM, NET_NUM, EXNET_NUM, SERVER_NUM, SUB_NUM)
    x = 100
    y = 60
    server_y = 10
    width = 180
    height = 110
    server_height = 100
    router_num = 0
    server_nmu = 0
    net_exnet_num = 0
    subnet_num = 0
    for i in range(len(tuopu_info['devices'])):
        if tuopu_info['devices'][i]['src'].endswith("server.png"):
            tuopu_info['devices'][i]['x'] = x + 4*width
            tuopu_info['devices'][i]['y'] = server_y + server_nmu*server_height
            server_nmu += 1
        if tuopu_info['devices'][i]['src'].endswith("router.png"):
            tuopu_info['devices'][i]['x'] = x + width
            tuopu_info['devices'][i]['y'] = y + router_num*height
            router_num += 1
        if tuopu_info['devices'][i]['src'].endswith("network.png"):
            tuopu_info['devices'][i]['x'] = x + 2*width
            tuopu_info['devices'][i]['y'] = y + height*net_exnet_num
            net_exnet_num += 1
        if tuopu_info['devices'][i]['src'].endswith("extnet.png"):
            tuopu_info['devices'][i]['x'] = 100
            tuopu_info['devices'][i]['y'] = y + height
            net_exnet_num += 1
        if tuopu_info['devices'][i]['src'].endswith("subnet.png"):
            tuopu_info['devices'][i]['x'] = 100 + 3*width
            tuopu_info['devices'][i]['y'] = y + height*subnet_num
            subnet_num += 1
    ROUTER_NUM = 0
    NET_NUM = 0
    EXNET_NUM = 0
    SERVER_NUM = 0
    SUB_NUM = 0
    return tuopu_info


