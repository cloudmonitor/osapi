# _*_ coding:utf-8 _*_

from identify import *
from nova import *
from topology import *
from neutron import *
from ceilometer import *
from firewall import *
from settings import *
from securitygroup import *
from floatingip import *
from quota import *
from keypair import *
from util import *
from user import *
from images import *


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
    token_json = get_tenant_token("project02", token_id)
    token_id = token_json['access']['token']['id']

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
    # print json.dumps(get_meter_func_data(token_id, "d88d4933-f0b4-48b9-bccf-2e458c430170", "cpu_util", "day"))
    # print json.dumps(get_meter_func_data(token_id, "f84d2a28-2bef-4075-94c3-de8ec36e52a4", "memory.usage", "minute"))
    # print json.dumps(get_tenant_instances(token_id, tenant_id))
    # print json.dumps(get_server_port(token_id, tenant_id))
    print delete_subnet(token_id, '{"subnet_ids":["d8f2be93-d772-491d-9827-d30bf20cc2d2","195030dc-9bf7-4c4d-a836-627e9ac757f6"]}')