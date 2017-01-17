# _*_ coding:utf-8 _*_

from osapi.settings import *

from osapi.flavors import get_flavor_name
from osapi.images import get_image_name


def get_all_tenant_instances(token_id, admin_tenant_id):
    """获取所有租户下所有的VM（超级管理员权限）"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=admin_tenant_id)
    r = requests.get(url+'/servers/detail?all_tenants=1', headers=headers)
    instances_info = r.json()
    for i in range(len(instances_info['servers'])):
        ret = requests.get(url + '/servers/' + instances_info['servers'][i]['id'] + "/os-interface", headers=headers)
        instances_info['servers'][i]['interfaceAttachments'] = ret.json()['interfaceAttachments']
        flavor_name = get_flavor_name(token_id, admin_tenant_id, instances_info['servers'][i]["flavor"]["id"])
        instances_info['servers'][i]["flavor"]["flavor_name"] = flavor_name
        image_name = get_image_name(token_id, instances_info['servers'][i]["image"]["id"])
        instances_info['servers'][i]['image']['image_name'] = image_name
    return instances_info


def get_hypervisor_instances(token_id, admin_tenant_id, hypervisor_name):
    """获取计算节点上所有的VM以及相应接口信息（超级管理员权限）"""
    hypervisor_servers_list = []
    all_instance_info = get_all_tenant_instances(token_id, admin_tenant_id)
    for instance in all_instance_info['servers']:
        if instance['OS-EXT-SRV-ATTR:hypervisor_hostname'] == hypervisor_name:
            hypervisor_servers_list.append(instance)
    return hypervisor_servers_list


if __name__ == "__main__":
    from osapi.identify import get_admin_token
    admin_token = get_admin_token("admin", "admin")
    admin_token_id = admin_token['access']['token']['id']
    admin_tenant_id = admin_token['access']['token']['tenant']['id']
    print json.dumps(get_all_tenant_instances(admin_token_id, admin_tenant_id))
    print json.dumps(get_hypervisor_instances(admin_token_id, admin_tenant_id, "compute01"))
