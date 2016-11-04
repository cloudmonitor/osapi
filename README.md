# 对OpenStack提供的api进行了封装提取

###安装

```bash
python setup.py install
```

###使用
```python
import osapi
token_json = osapi.get_user_token("admin", "admin")
print token_json
```

###输出
```json
{"access": {"token": {"issued_at": "2016-11-04T08:44:39.961544", "expires": "2016-11-04T09:44:39Z", "id": "aa47ab55ff0f4492a1f38abb0a98c3a0", "audit_ids": ["bj_gTCq-RBOz3icCMQFhWw"]}, "serviceCatalog": [], "user": {"username": "user01", "roles_links": [], "id": "b3316fd36b58436aa035bf3844deb768", "roles": [], "name": "user01"}, "metadata": {"is_admin": 0, "roles": []}}}

```