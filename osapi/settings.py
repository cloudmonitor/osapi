# _*_ coding:utf-8 _*_

"""主要定义一些Openstack认证json字符串以及各模块方位的URL"""

import requests
import json
import time
import datetime


CREDENTIAL_PASSWORD = '{"auth": {"tenantName": "%s", "passwordCredentials": {"username": "%s", "password": "%s"}}}'
CREDENTIAL_TOKEN = '{"auth":{"tenantName":"%s","token":{"id":"%s"}}}'

KEYSTONE_ENDPOINT = 'http://controller:5000/v2.0'
GLANCE_ENDPOINT = 'http://controller:9292/v2'
NOVA_ENDPOINT = 'http://controller:8774/v2/{tenant_id}'
NOVA_ENDPOINT01 = 'http://controller:8774/v2/bcfa01f3cd9b421a80705224ad356f63'
NEUTRON_ENDPOINT = 'http://controller:9696/v2.0'
CEILOMETER_ENDPOINT = 'http://controller:8777/v2'
KEYSTONE_ENDPOINT01 = "http://controller:35357/v2.0/users"