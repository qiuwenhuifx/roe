# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from CMDB.model.yewutree_model import YewuTreeMptt as YewuTree
from django.contrib.auth.models import User

MyARCH = (
    (u"主从", u"主从"),
    (u"单库", u"单库"),
    (u"innodb_cluster", u"innodb_cluster"),
    (u"PXC", u"PXC")
)

MyDB_ROLE = (
    (u"单库", u"单库"),
    (u"主库", u"主库"),
    (u"从库", u"从库"),
    (u"汇总", u"汇总")
)

MyDB_STATUS = (
    (u"服务中", u"服务中"),
    (u"仅从库", u"仅从库"),
    (u"故障", u"故障"),
    (u"其他", u"其他"),
)
#群，一定属于某一个产品线，可能属于多个组,一个节点也是群
class MySQLCluster(models.Model):
    name = models.CharField(u"集群名", max_length=30, blank=True,null=True)
    arch = models.CharField(verbose_name=u"集群架构",choices=MyARCH, max_length=30, null=True, blank=True)
    db_version = models.CharField(verbose_name=u"数据库版本",  max_length=30, null=True, blank=True)
    foreign_ip=models.CharField(verbose_name=u"集群对外IP",  max_length=30, null=True, blank=True)
    foreign_port = models.IntegerField(verbose_name=u"集群对外端口",  null=True, blank=True)
    plat_user=models.CharField(verbose_name=u"平台操作用户",  max_length=30, null=True, blank=True)
    plat_user_pass=models.CharField(verbose_name=u"平台操作用户密码",  max_length=60, null=True, blank=True)
    domain=models.CharField(verbose_name=u"集群对外域名", max_length=100, null=True, blank=True)
    tree_id=models.ForeignKey(YewuTree,verbose_name=u"所属产品线", on_delete=models.SET_NULL, null=True, blank=True)
    desc = models.CharField(u"描述", max_length=100, null=True, blank=True)
    operator = models.ForeignKey(User, verbose_name="可见的人", blank=True,null=True)
    status=models.CharField(u"状态", max_length=30, blank=True,null=True)
    is_pooled=models.BooleanField(verbose_name='是否在资源池中',default=True,blank=True) #在资源池中的数据才能被分配给业务,同时本资源移出资源池,不再在业务中和资源池中的表明还没准备好
    up_date = models.CharField(max_length=30,null=True, blank=True, verbose_name=u'上线日期')
    down_date = models.CharField(max_length=30,null=True, blank=True, verbose_name=u'下线日期')
    def __unicode__(self):
        return self.name
    class Meta:
        db_table = 'MySQL_Cluster'
        permissions = (
            ("can_read_mysql_cluster", "读取资产权限"),
            ("can_change_mysql_cluster", "更改资产权限"),
            ("can_add_mysql_cluster", "添加资产权限"),
            ("can_delete_mysql_cluster", "删除资产权限"),
            ("can_dumps_mysql_cluster", "导出资产权限"),
        )
        verbose_name = 'mysql集群'
        verbose_name_plural = 'mysql集群'




#数据库内用户 密码放在集群下，不妨在 实例中。
class Mysql_User(models.Model):
    db_user = models.CharField(max_length=60, null=True,blank=True)
    db_host = models.CharField(max_length=20, null=True,blank=True)
    db_password=models.CharField(max_length=60, null=True,blank=True)
    privlige=models.CharField(verbose_name='权限',max_length=4000, null=True,blank=True)
    dbcluster = models.ForeignKey(MySQLCluster,verbose_name=u"所属集群",related_name='mysql_user' , null=True, blank=True)
    memo = models.CharField(max_length=50, verbose_name=u"备注", blank=True, null=True)
    def __unicode__(self):
        return self.db_user
    class Meta:
        db_table = 'MySQL_User'
        verbose_name = 'mysql内部用户'
        verbose_name_plural = 'mysql内部用户'

#数据库中的 DB，表空间信息
class Mysql_db(models.Model):
        dbname = models.CharField(max_length=50,verbose_name=u"数据库或表空间名")
        index_size = models.FloatField( verbose_name=u"索引大小Mb", blank=True, null=True)
        db_size = models.FloatField( verbose_name=u"库大小(Mb)", blank=True, null=True)
        db_rows=models.IntegerField( verbose_name=u"库大小(Mb)", blank=True, null=True)
        dbcluster = models.ForeignKey(MySQLCluster,verbose_name=u"所属集群", related_name='mysql_db', null=True, blank=True)
        memo=models.CharField(max_length=50,verbose_name=u"备注",blank=True,null=True)
        def __unicode__(self):
            return u'%s ' % ( self.dbname)

        class Meta:
            db_table = 'MySQL_DB'
            verbose_name = 'mysql内部DB'
            verbose_name_plural = 'mysql内部DB'

# Mysql DB 单,主从都写在这里，配置文件的参数，变量慢慢添加
class MySQL_Instance(models.Model):
        dbtag = models.CharField(max_length=50, verbose_name=u"数据库实例标签")
        vist_ip = models.GenericIPAddressField(verbose_name=u"访问IP", max_length=15,blank=True,null=True)
        m_ip = models.GenericIPAddressField(verbose_name=u"管理IP", max_length=15)
        port = models.CharField(verbose_name=u"端口", max_length=5)
        master_ip = models.GenericIPAddressField(verbose_name=u"他的主库IP", max_length=15, null=True, blank=True)
        master_port = models.CharField(verbose_name=u"他的主库端口", max_length=6, null=True, blank=True)
        idc =  models.CharField(verbose_name=u"机房", max_length=60, null=True, blank=True)
        dbcluster = models.ForeignKey(to="MySQLCluster", related_name='mysql_instance', null=True, blank=True)
        role = models.CharField(verbose_name=u"DB角色", choices=MyDB_ROLE, max_length=50,null=True, blank=True)
        db_status = models.CharField(verbose_name=u"DB状态", choices=MyDB_STATUS, max_length=30, null=True, blank=True)
        memory = models.CharField(u"分配内存", max_length=30, null=True, blank=True)
        disk = models.CharField(u"磁盘位置", max_length=255, null=True, blank=True)
        memo = models.TextField(u"备注信息", max_length=200, null=True, blank=True)

        def __unicode__(self):
            return self.dbtag
        class Meta:
            unique_together=('m_ip','port')
            db_table = 'MySQL_Instance'
            verbose_name = 'mysql_Instance'
            verbose_name_plural = verbose_name