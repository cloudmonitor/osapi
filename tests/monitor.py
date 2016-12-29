# _*_ coding:utf-8 _*_

from osapi.identify import *
from osapi.nova import *
from osapi.topology import *
from osapi.neutron import *
from osapi.ceilometer import *
from osapi.firewall import *
from osapi.settings import *
from osapi.securitygroup import *
from osapi.floatingip import *
from osapi.quota import *
from osapi.keypair import *
from osapi.util import *
from osapi.user import *
from osapi.images import *
# from osapi.nova import get_tenant_instance_inteface


if __name__ == "__main__":

    # 通过用户和密码获取token
    token_json = get_user_token("user01", "user01")
    admin_json = get_admin_token()
    token = token_json['access']['token']
    token_id = token_json['access']['token']['id']
    admin_token_id = admin_json['access']['token']['id']
    # 获取租户
    # print get_tenants(token_id)
    # tenant_name = get_tenants(token_id)['tenants'][0]['name']
    tenant_id = get_tenants(token_id)['tenants'][0]['id']
    # 获取租户的token
    token_json = get_tenant_token("project01", token_id)
    token_id = token_json['access']['token']['id']
    tenant_id = token_json['access']['token']['tenant']['id']


    # print get_tenant_used_info(token_id,tenant_id)

    # delete_port_list = get_dis_port(token_id)
    # print delete_port_list
    # print delete_port(token_id,delete_port_list)
    # print json.dumps(get_tenant_networks(token_id))
    # print json.dumps(get_last_network_topology(token_id, tenant_id))
    # print json.dumps(get_network_servers(token_id, tenant_id, "447e39f3-7710-48b4-9fd8-3356511f8c83"))
    # print json.dumps(get_tenant_instances(token_id, tenant_id))
    # print json.dumps(get_router_networks(token_id, "d2092658-6162-49c7-b5a5-94380256e995"))
    # print get_router_servers(token_id, tenant_id, "d2092658-6162-49c7-b5a5-94380256e995")
    # print json.dumps(get_last_network_topology(token_id, tenant_id))
    # print json.dumps(get_tenant_instances(token_id, tenant_id))
    # print json.dumps(get_tenant_subnets(token_id))
    # print json.dumps(remove_router_interface(token_id, "d2092658-6162-49c7-b5a5-94380256e995", '{"router_ports":["f38be73c-fc0f-420e-bf0b-965c7613d6aa"]}'))
    # print json.dumps(ports_network(token_id))
    # print json.dumps(router_network(token_id,tenant_id))
    # print json.dumps(get_server_console(token_id, tenant_id, "664a8a84-d9b4-43fe-ba23-31b561e35907", '{"os-getVNCConsole": {"type": "novnc"}}'))
    # print json.dumps(router_network(token_id, tenant_id))
    # print json.dumps(get_last_network_topology(token_id, tenant_id))
    # print json.dumps(get_meter_func_data(token_id, "a26d27a1-88da-485f-ab84-1f484bce78eb", "cpu_util", "minute", 1))
    # print json.dumps(get_meter_func_data(token_id, "b18ff7c9-70cc-4781-ad31-af9845e005db", "disk.read.bytes.rate", "minute", 1))
    # print json.dumps(get_tenant_instances(token_id, tenant_id))
    # print json.dumps(get_server_port(token_id, tenant_id))
    # print delete_subnet(token_id, '{"subnet_ids":["d8f2be93-d772-491d-9827-d30bf20cc2d2","195030dc-9bf7-4c4d-a836-627e9ac757f6"]}')
    # print json.dumps(get_hypervisor_instances_and_interface())
    # print json.dumps(get_tenant_instance(token_id, tenant_id, "3d77c37a-a67e-43b9-a10d-f037472a5319"))
    # print json.dumps(get_server_interface(token_id, tenant_id, "3d77c37a-a67e-43b9-a10d-f037472a5319"))
    # print json.dumps(get_tenant_instance_inteface(token_id, tenant_id, "3d77c37a-a67e-43b9-a10d-f037472a5319"))
    # print json.dumps(get_tenant_instance_host_ip(token_id, tenant_id, "3d77c37a-a67e-43b9-a10d-f037472a5319"))



