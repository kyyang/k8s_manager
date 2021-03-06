# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from . import common
# Create your models here.
# python manage.py migrate   # create table
# python manage.py makemigrations k8s_manager   # change model
# python manage.py migrate k8s_manager   # create table

class Assets(models.Model):

    product_name = models.CharField(max_length=50)
    assets_type = models.IntegerField(choices=common.TYPE_VALUE)
    status = models.IntegerField(choices=common.STATUS_VALUE)
    active_date = models.DateField(blank=True,null=True)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    create_user = models.CharField(max_length=20)
    update_user = models.CharField(max_length=20)
    idc = models.CharField(max_length=200)
    cabinet_no = models.CharField(max_length=200)
    cabinet_order = models.CharField(max_length=200)
    tags = models.CharField(max_length=200)

    class Meta:
        db_table = "assets"


class Product(models.Model):
    product_name = models.CharField(max_length=50)
    product_desc = models.CharField(max_length=255)
    product_status = models.CharField(max_length=50)
    product_manager = models.CharField(max_length=20)
    product_contact = models.CharField(max_length=50)

    dev_manager = models.CharField(max_length=20)
    dev_contact = models.CharField(max_length=50)
    qa_manager = models.CharField(max_length=20)
    qa_contact = models.CharField(max_length=50)
    safe_manager = models.CharField(max_length=20)
    safe_contact = models.CharField(max_length=50)

    online_version = models.CharField(max_length=30)
    product_wiki = models.CharField(max_length=200)

    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now = True)
    create_user = models.CharField(max_length=20)
    update_user = models.CharField(max_length=20)

    last_online = models.DateField(blank=True,null=True)
    product_tags = models.CharField(max_length=255)

    class Meta:
        db_table = "product"


class ProductVersion(models.Model):
    product_id = models.IntegerField()
    version_name = models.CharField(max_length=20)
    product_manager = models.CharField(max_length=20)
    start_time = models.DateField()
    end_time = models.DateField()

    version_wiki = models.CharField(max_length=255)
    version_status = models.IntegerField()
    version_env = models.IntegerField(null=True,blank=True)

    product_contact = models.CharField(max_length=50)
    dev_manager = models.CharField(max_length=20)
    dev_contact = models.CharField(max_length=50)
    qa_manager = models.CharField(max_length=20)
    qa_contact = models.CharField(max_length=50)
    safe_manager = models.CharField(max_length=20)
    safe_contact = models.CharField(max_length=50)

    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now = True)
    create_user = models.CharField(max_length=20)
    update_user = models.CharField(max_length=20)

    tags = models.CharField(max_length=255)

    class Meta:
        db_table = "product_version"


class KubeConfig(models.Model):
    # 集群名称/标识，如 Test
    kube_name = models.CharField(max_length=20)
    # 集群主版本号, 如 v1.8, v1.9, v1.10，v1.11, v1.12
    kube_version = models.CharField(max_length=20,choices=common.K8S_VERSION)
    # 集群部署模式：allinone, single-master, multi-master
    deploy_mode = models.CharField(max_length=20,choices=common.K8S_DEPLOY_MODE)
    #部署节点ip
    deploy_node = models.CharField(max_length=30,blank=True,null=True)
    # 集群是否安装 chrony 时间同步,yes/no
    ntp_enabled = models.CharField(max_length=10)

    # 是否自动配置免密钥
    ssh_addkey = models.CharField(max_length=10,choices=common.COMMON_STATUS)

    # 服务端口范围 (NodePort Range),如：20000-40000
    node_port_range = models.CharField(max_length=20)
    
    # master_ip即LB节点VIP地址，为区别与默认apiserver端口，设置VIP监听的服务端口8443
    # 公有云上请使用云负载均衡内网地址和监听端口
    master_ip = models.CharField(max_length=20)
    kube_api_server = models.CharField(max_length=100)

    # 集群网络插件，目前支持calico, flannel, kube-router, cilium
    cluster_network = models.CharField(max_length=20,choices=common.K8S_CLUSTER_NETWORK)

    # 服务网段 (Service CIDR），注意不要与内网已有网段冲突
    service_cidr = models.CharField(max_length=40)
    # POD 网段 (Cluster CIDR），注意不要与内网已有网段冲突
    cluster_cidr = models.CharField(max_length=40)
    # kubernetes 服务 IP (预分配，一般是 SERVICE_CIDR 中第一个IP)
    cluster_k8s_svc_ip = models.CharField(max_length=40)
    # 集群 DNS 服务 IP (从 SERVICE_CIDR 中预分配)
    cluster_dns_svc_ip = models.CharField(max_length=40)
    # 集群 DNS 域名
    cluster_dns_domain = models.CharField(max_length=40)

    # 集群basic auth 使用的用户名和密码
    basic_auth_user = models.CharField(max_length=40)
    basic_auth_pass = models.CharField(max_length=40)

    # 默认二进制文件目录
    bin_dir = models.CharField(max_length=40)
    # 证书目录
    ca_dir = models.CharField(max_length=40)
    # 部署目录，即 ansible 工作目录，建议不要修改
    base_dir = models.CharField(max_length=40)

    # 该集群是否已经部署
    deploy = models.CharField(max_length=5,choices=common.COMMON_STATUS,blank=True,null=True)
    # 该集群部署错误信息
    deploy_error = models.CharField(max_length=255)

    # 部署状态
    deploy_status = models.IntegerField(null=True,blank=True)
    
    # 集群描述信息
    kube_desc = models.CharField(max_length=255)

    create_date = models.DateField(auto_now_add=True)
    create_user = models.CharField(max_length=20)
    update_date = models.DateField(auto_now = True)
    update_user = models.CharField(max_length=20)

    class Meta:
        db_table = "kube_config"


class KubeCluster(models.Model):
    # 集群id，唯一标识
    kube_id = models.IntegerField()
    # 节点ip
    node_ip = models.CharField(max_length=20)
    # 节点域名
    node_domain = models.CharField(max_length=40,blank=True,null=True)
    # 节点类型
    node_type = models.CharField(max_length=40,choices=common.K8S_NODE_TYPE)
    # 节点用户名
    node_user = models.CharField(max_length=30)
    # 节点密码
    node_password = models.CharField(max_length=100)
    # 节点端口号
    node_port = models.IntegerField(null=True,blank=True)
    # 节点主机名
    node_name = models.CharField(max_length=50,blank=True,null=True)
    # 节点角色，如: master/backup
    node_role = models.CharField(max_length=10,choices=common.K8S_NODE_ROLE)
    # 是否已经配置过ssh免密钥登陆
    ssh_enabled = models.CharField(max_length=5,choices=common.COMMON_STATUS,blank=True,null=True)
    # 安装类型 yes为新安装 no为使用已有服务器
    install_type = models.CharField(max_length=5,choices=common.COMMON_STATUS,blank=True,null=True)
    # 节点状态
    node_status = models.IntegerField(choices=common.K8S_NODE_STATUS,blank=True,null=True)
    # 创建日期
    create_date = models.DateField(auto_now_add=True)
    # 修改日期
    update_date = models.DateField(auto_now = True)
    class Meta:
        db_table = "kube_cluster"

# k8s集群安装验证命令手册
class InstallCheck(models.Model):
     # 命令名称，展示用
    command_name = models.CharField(max_length=30)
    # 命令
    command = models.CharField(max_length=500)
    # 命令所属类别，如etcd/集群pod状态等
    command_category = models.CharField(max_length=20,null=True,blank=True)
    # 是否可执行
    command_exec = models.CharField(max_length=5,choices=common.COMMON_STATUS)
    # 命令描述
    command_desc = models.CharField(max_length=500,null=True,blank=True)

    class Meta:
        db_table = "install_check"

class InstallStep(models.Model):
    # 步骤id，不可以重复
    step_id = models.IntegerField(primary_key=True)
    # 要执行该步骤，当前步骤最小值，如：安装master之前，需要先配置免密钥登陆
    last_step_id = models.IntegerField(null=True,blank=True)
    # 步骤名称，展示用
    step_name = models.CharField(max_length=20)
    # 安装该步骤，需要调用的安装函数
    step_function = models.CharField(max_length=40)
    # 安装函数执行前需调用的函数
    step_before_function = models.CharField(max_length=40,null=True,blank=True)
    # 安装函数执行后需调用的函数
    step_after_function = models.CharField(max_length=40,null=True,blank=True)
    # 步骤所属分类，如：安装准备/分步安装/一键安装等，展示用
    step_category = models.IntegerField(choices=common.INSTALL_STEP_CATEGORY)
    # 该步骤是否可以跳过，意味着该步骤不是强制安装
    step_skip = models.CharField(max_length=5,choices=common.COMMON_STATUS)
    # 该步骤使用的yml文件
    step_yml_file = models.CharField(max_length=100,null=True,blank=True)
    # 该步骤使用的yml文件拷贝，例如：yml_file文件是个模板文件，不针对模板文件操作，而是拷贝出来一份，在临时文件中操作，然后删除掉临时文件
    step_yml_file_tmp = models.CharField(max_length=100,null=True,blank=True)
    # 该步骤在当前类别下的顺序值
    step_sort = models.IntegerField(null=True,blank=True)
    # 步骤描述
    step_desc = models.CharField(max_length=200,null=True,blank=True)
    
    class Meta:
        db_table = "install_step"


class InstallLock(models.Model):
    # 集群id
    kube_id = models.IntegerField()
    # 自定义key
    lock_key = models.CharField(max_length=30)
    create_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('kube_id','lock_key',)
        db_table = "install_lock"


class Server(models.Model):
    id = models.IntegerField(primary_key=True)
    manage_ip = models.CharField(max_length=255)
    sn = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    platform = models.CharField(max_length=255)
    version = models.CharField(max_length=40)
    cpu_count = models.IntegerField(null=True,blank=True)
    cpu_physical_count = models.IntegerField(null=True,blank=True)
    cpu_model = models.CharField(max_length=255)
    
    mac = models.CharField(max_length=255)
    serial_num = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    port_num = models.IntegerField(null=True,blank=True)
    intranet_ip = models.CharField(max_length=255)
    user = models.CharField(max_length=255)
    ip = models.CharField(max_length=255)
    port = models.IntegerField()
    desc = models.CharField(max_length=255)

    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now = True)
    create_user = models.CharField(max_length=20)
    update_user = models.CharField(max_length=20)

    class Meta:
        db_table = "server"

class Template(models.Model):
    name = models.CharField(max_length=20)
    path = models.CharField(max_length=50)
    tag = models.CharField(max_length=100)
    status = models.IntegerField()
    create_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "template"


class VersionEnv(models.Model):
    version_id = models.IntegerField()
    tag = models.CharField(max_length=255)
    env = models.IntegerField()
    image_type = models.IntegerField(null=True,blank=True)
    deploy_type = models.IntegerField(null=True,blank=True)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now = True)
    create_user = models.CharField(max_length=20)
    update_user = models.CharField(max_length=20)

    class Meta:
        db_table = "version_env"









