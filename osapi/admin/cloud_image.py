# _*_ coding:utf-8 _*_


from osapi.settings import *
import os
from osapi.identify import get_admin_token


def get_all_images(token_id):
    """获取所有的镜像信息"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = GLANCE_ENDPOINT + "/images"
    r = requests.get(url=url, headers=headers)
    return r.json()


def allowed_file(filename):
    """用于镜像上传的文件名后缀是否合法"""
    ALLOWED_EXTENSIONS = set(['qcow2', 'ami', 'ari', 'aki', 'vhd', 'vhdx', 'vmdk', 'raw', 'vdi', 'iso'])  # 文件末尾名集合
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def upload_image_info(token_id, image_id, file):
    """上传镜像文件"""
    print file
    headers = {"Content-type": "application/octet-stream", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = GLANCE_ENDPOINT + "/images/"+image_id+"/file"
    r = requests.put(url=url, headers=headers, data=file)
    return r.status_code


def create_image(token_id, data, file_name):
    """上传创建镜像信息"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = GLANCE_ENDPOINT + "/images"
    r = requests.post(url=url, data=data, headers=headers)
    image_info = r.json()
    image_id = image_info['id']
    basedir = os.path.abspath('..//..//..')  # 获取本项目根目录的上一级目录
    file_dir = os.path.join(basedir, 'cloudmonitor', 'upload', file_name)
    image_info_bak = upload_image_info(token_id, image_id, file_dir)
    os.remove(file_dir)
    return image_info_bak


def delete_image(admin_token_id, images_id_list):
    """删除云镜像"""
    print images_id_list
    images_id_list = json.loads(images_id_list)
    delete_status = {}
    headers = {"Content-type": "application/json", "X-Auth-Token": admin_token_id, "Accept": "application/json"}
    for i in range(len(images_id_list["images_ids"])):
        url = GLANCE_ENDPOINT + "/images/"+images_id_list["images_ids"][i]
        print url
        r = requests.delete(url=url, headers=headers)
        delete_status[images_id_list["images_ids"][i]] = r.status_code
    return delete_status


def update_image(admin_token_id, image_id, data):
    """更新云镜像"""
    headers = {"Content-type": "application/openstack-images-v2.1-json-patch", "X-Auth-Token": admin_token_id, "Accept": "application/json"}
    url = GLANCE_ENDPOINT + "/images/"+image_id
    r = requests.patch(url=url, headers=headers, data=data)
    return r.json()


if __name__ == "__main__":
    admin_json = get_admin_token("admin", "admin")
    admin_tenant_id = admin_json['access']['token']['tenant']['id']
    admin_token_id = admin_json['access']['token']['id']
    # print json.dumps(create_image(admin_token_id, '{"container_format": "bare","name": "Ubuntu","disk_format":"qcow2","min_disk" :0,"min_ram":0,"protected":false,"visibility" :"private"}', "109.iso"))
    print json.dumps(delete_image(admin_token_id, '{"images_ids": ["bb22be0d-5a03-43c2-92fb-d4f858178d63"]}'))

