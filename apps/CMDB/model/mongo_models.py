# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from CMDB.model.yewutree_model import YewuTree
from django.contrib.auth.models import User

MONGOARCH=(
    (u"副本集",u"副本集"),
    (u"单机",u"单击"),
    (u"分片",u"分片"),
)

MongoDB_ROLE = (
    (u"单库", u"单库"),
    (u"主库", u"主库"),
    (u"从库", u"从库"),
    (u"汇总", u"汇总")
    )


MongoDB_STATUS = (
    (u"使用中", u"使用中"),
    (u"未使用", u"未使用"),
    (u"故障", u"故障"),
    (u"其它", u"其它"),
    )



#群，一定属于某一个产品线，可能属于多个组,一个节点也是群
class MongoCluster(models.Model):
    name = models.CharField(u"集群名", max_length=30, blank=True,null=True)
    arch = models.CharField(verbose_name=u"集群架构", choices=MONGOARCH,max_length=30, null=True, blank=True)
    db_version = models.CharField(verbose_name=u"数据库版本",  max_length=30, null=True, blank=True)
    defaultdb=models.CharField(verbose_name=u"主用DB",  max_length=30, null=True, blank=True)
    tree_id=models.ForeignKey(YewuTree,verbose_name=u"所属业务线", on_delete=models.SET_NULL, null=True, blank=True)
    desc = models.CharField(u"描述", max_length=100, null=True, blank=True)
    is_pooled=models.BooleanField(verbose_name='是否在资源池中',default=True,blank=True) #在资源池中的数据才能被分配给业务,同时本资源移出资源池,不再在业务中和资源池中的
    operator = models.ForeignKey(User, verbose_name=u"可操作的人", blank=True)
    class meta:
        db_table='mongocluster'
        verbose_name = 'mongo cluster'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name



#数据库内用户 密码放在集群下，不妨在 实例中。
class MongoDBUser(models.Model):
    db_user = models.CharField(max_length=30, null=True,blank=True)
    db_password=models.CharField(max_length=60, null=True,blank=True)
    privlige=models.CharField(verbose_name=u'权限',max_length=200, null=True,blank=True)
    dbcluster = models.ForeignKey(MongoCluster,verbose_name=u"所属集群", on_delete=models.SET_NULL, null=True, blank=True)

    class meta:
        db_table = 'mongodb_user'
        verbose_name = 'mongo cluster'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.db_user


#数据库中的 DB，表空间信息
class MongoDBName(models.Model):
        dbname = models.CharField(max_length=50,verbose_name=u"数据库名")
        dbcluster = models.ForeignKey(MongoCluster,verbose_name=u"所属集群", on_delete=models.SET_NULL, null=True, blank=True)
        db_size=models.CharField(max_length=50,verbose_name=u"库大小")

        class meta:
            db_table = 'mongodb_dbname'
            verbose_name = 'mongo_dbname'
            verbose_name_plural = verbose_name
        def __unicode__(self):
            return u'%s ' % ( self.dbname)


#mongo实例
class Mongo_Instance(models.Model):
    dbtag = models.CharField(max_length=50, verbose_name=u"数据库标志", blank=True,null=True)
    vist_ip = models.GenericIPAddressField(verbose_name=u"访问VIP", max_length=15)
    m_ip =  models.GenericIPAddressField(verbose_name=u"管理IP", max_length=15)
    other_ip= models.CharField(max_length=150, verbose_name=u"其他IP,逗号隔开")
    port = models.IntegerField(verbose_name=u"端口",default=27017)
    idc = models.CharField( verbose_name=u"机房",  null=True, blank=True)
    dbcluster = models.ForeignKey(MongoCluster, verbose_name=u"所属集群", on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(verbose_name=u"实例", choices=MongoDB_ROLE, max_length=30, null=True, blank=True)
    db_status = models.CharField(verbose_name=u"DB状态", choices=MongoDB_ROLE, max_length=30, null=True, blank=True)
    memory = models.CharField(verbose_name=u"分配内存", max_length=30, null=True, blank=True)
    disk = models.CharField(verbose_name=u"磁盘位置", max_length=200, null=True, blank=True)
    memo = models.TextField(verbose_name=u"备注信息", max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.dbtag


    class meta:
        db_table = 'mongodb_instance'
        verbose_name = 'mongo instance'
        verbose_name_plural = verbose_name

