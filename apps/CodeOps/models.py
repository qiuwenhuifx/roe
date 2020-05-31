#!/usr/bin/env python
# _#_ coding:utf-8 _*_
from django.db import models
import sys


reload(sys)
sys.setdefaultencoding("utf-8")

class Project_Assets(models.Model):
    '''产品线资产表'''
    project_name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'project_assets'
        permissions = (
            ("can_read_project_assets", "读取产品线权限"),
            ("can_change_project_assets", "更改产品线权限"),
            ("can_add_project_assets", "添加产品线权限"),
            ("can_delete_project_assets", "删除产品线权限"),
        )
        verbose_name = '项目资产表'
        verbose_name_plural = '项目资产表'



class Service_Assets(models.Model):
    '''业务分组表'''
    project = models.ForeignKey('Project_Assets', related_name='service_assets', on_delete=models.CASCADE)
    service_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'service_assets'
        permissions = (
            ("can_read_service_assets", "读取业务资产权限"),
            ("can_change_service_assets", "更改业务资产权限"),
            ("can_add_service_assets", "添加业务资产权限"),
            ("can_delete_service_assets", "删除业务资产权限"),
        )
        unique_together = (("project", "service_name"))
        verbose_name = '业务分组表'
        verbose_name_plural = '业务分组表'


class Project_Config(models.Model):
    project_repertory_choices = (
        ('git', u'git'),
        ('svn', u'svn'),
    )
    deploy_model_choices = (
        ('branch', u'branch'),
        ('tag', u'tag'),
    )
    project = models.ForeignKey('Project_Assets', related_name='project_config', on_delete=models.CASCADE)
    project_env = models.CharField(max_length=50, verbose_name='项目环境', default=None)
    project_name = models.CharField(max_length=100, verbose_name='项目名称', default=None)
    project_service = models.SmallIntegerField(verbose_name='业务类型')
    project_type = models.CharField(max_length=20, verbose_name='编译类型', blank=True, null=True)
    project_local_command = models.TextField(blank=True, null=True, verbose_name='部署服务器要执行的命令', default=None)
    project_repo_dir = models.CharField(max_length=100, verbose_name='本地仓库目录', default=None)
    project_dir = models.CharField(max_length=100, verbose_name='代码目录', default=None)
    project_exclude = models.TextField(blank=True, null=True, verbose_name='排除文件', default=None)
    project_address = models.CharField(max_length=100, verbose_name='版本仓库地址', default=None)
    project_uuid = models.CharField(max_length=50, verbose_name='唯一id')
    project_repo_user = models.CharField(max_length=50, verbose_name='仓库用户名', blank=True, null=True)
    project_repo_passwd = models.CharField(max_length=50, verbose_name='仓库密码', blank=True, null=True)
    project_repertory = models.CharField(choices=project_repertory_choices, max_length=10, verbose_name='仓库类型',
                                         default=None)
    project_status = models.SmallIntegerField(verbose_name='是否激活', blank=True, null=True, default=None)
    project_remote_command = models.TextField(blank=True, null=True, verbose_name='部署之后执行的命令', default=None)
    project_user = models.CharField(max_length=50, verbose_name='项目文件宿主', default=None)
    project_model = models.CharField(choices=deploy_model_choices, max_length=10, verbose_name='上线类型', default=None)
    project_audit_group = models.SmallIntegerField(verbose_name='项目授权组', blank=True, null=True, default=None)
    '''自定义权限'''

    class Meta:
        db_table = 'project_config'
        permissions = (
            ("can_read_project_config", "读取项目部署权限"),
            ("can_change_project_config", "更改项目部署权限"),
            ("can_add_project_config", "添加项目部署权限"),
            ("can_delete_project_config", "删除项目部署权限"),
        )
        unique_together = (("project_env", "project", "project_name"))
        verbose_name = '项目管理表'
        verbose_name_plural = '项目管理表'


class Log_Project_Config(models.Model):
    project_id = models.IntegerField(verbose_name='项目id', blank=True, null=True, default=None)
    project_user = models.CharField(max_length=50, verbose_name='操作用户', default=None)
    project_name = models.CharField(max_length=100, verbose_name='名称', default=None)
    project_content = models.CharField(max_length=100, default=None)
    project_branch = models.CharField(max_length=100, default=None, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='执行时间')

    class Meta:
        db_table = 'log_project_config'
        verbose_name = '项目配置操作记录表'
        verbose_name_plural = '项目配置操作记录表'


class Project_Number(models.Model):
    project = models.ForeignKey('Project_Config', related_name='project_number', on_delete=models.CASCADE)
    server = models.CharField(max_length=100, verbose_name='服务器IP', default=None)
    dir = models.CharField(max_length=100, verbose_name='项目目录', default=None)

    class Meta:
        db_table = 'project_number'
        unique_together = (("project", "server"))
        verbose_name = '项目成员表'
        verbose_name_plural = '项目成员表'

    def __unicode__(self):
        return '%s,%s' % (self.server, self.dir)