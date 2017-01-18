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
from osapi.admin.abstract import *
from osapi.admin.physical_host import *
from osapi.admin.tenant_user import *
from osapi.admin.tenant_resource import *
from osapi.nova import get_tenant_instance_inteface
from osapi.sdnapi.settings import OPENFLOWDB_CONN, BASE_URL
from osapi.sdnapi import Controller, StaticFlowPusher
from osapi.mongodbconn import MongoHelper


if __name__ == "__main__":

    # 通过用户和密码获取token
    token_json = get_user_token("user01", "user01")
    admin_json = get_admin_token("admin", "admin")
    token = token_json['access']['token']
    token_id = token_json['access']['token']['id']
    admin_token_id = admin_json['access']['token']['id']
    admin_tenant_id = admin_json['access']['token']['tenant']['id']
    # print admin_tenant_id
    # print admin_token_id
    # 获取租户
    # print get_tenants(token_id)
    # tenant_name = get_tenants(token_id)['tenants'][0]['name']
    tenant_id = get_tenants(token_id)['tenants'][0]['id']
    # 获取租户的token
    # token_json = get_tenant_token("project01", token_id)
    # token_id = token_json['access']['token']['id']
    # tenant_id = token_json['access']['token']['tenant']['id']
    # print tenant_id

    # print get_tenant_used_info(token_id,tenant_id)

    # print delete_subnet(token_id, '{"subnet_ids":["d8f2be93-d772-491d-9827-d30bf20cc2d2","195030dc-9bf7-4c4d-a836-627e9ac757f6"]}')
    # print json.dumps(get_hypervisor_instances_and_interface())
    # print json.dumps(get_tenant_instance(token_id, tenant_id, "3d77c37a-a67e-43b9-a10d-f037472a5319"))
    # print json.dumps(get_server_interface(token_id, tenant_id, "3d77c37a-a67e-43b9-a10d-f037472a5319"))
    # print json.dumps(get_tenant_instance_inteface(token_id, tenant_id, "3d77c37a-a67e-43b9-a10d-f037472a5319"))
    # print json.dumps(get_tenant_instance_host_ip(token_id, tenant_id, "3d77c37a-a67e-43b9-a10d-f037472a5319"))
    # print json.dumps(get_abstarct_info(admin_token_id, "2017-01-01 00:00:00.000000", "2017-01-18 08:00:00.000000", admin_tenant_id))
    # print json.dumps(get_physical_usage(admin_token_id, admin_tenant_id))
    # print json.dumps(get_statistics_info(admin_token_id, admin_tenant_id))
    # print json.dumps(get_hypervisor_info(admin_token_id, admin_tenant_id, "1"))
    # print json.dumps(get_users_list(admin_token_id))
    # print json.dumps(get_tenant_used_info(admin_token_id, admin_tenant_id))
    # print json.dumps(delete_tenant("2bcab976a7b24fb6b146a562c8829077", "4dfb08fcf39940759cf723729bbbad61"))
    # print json.dumps(delete_tenant(admin_token_id, "5c40e388d58040589e68fec04b20b2b8"))
    print json.dumps(delete_tanant_list(admin_token_id, '{"tenant_id": ["192c73c94f914e9599fccbb32070f5e5", "b5fd0f4bfe154095ab3f48b7623f854f"]}'))