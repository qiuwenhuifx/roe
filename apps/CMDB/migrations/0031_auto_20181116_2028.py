# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-16 12:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CMDB', '0030_auto_20181116_1841'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='yewutreemptt',
            name='root',
        ),
        migrations.AddField(
            model_name='yewutreemptt',
            name='yewuxian',
            field=models.ForeignKey(blank=True, help_text='\u6307\u5b9a\u6839\u7ed3\u70b9\u4e3a\u4ea7\u54c1\u7ebf\u8282\u70b9\uff0c\u4e3a\u4e86\u5c55\u793a\u4e1a\u52a1\u7ebf\u8282\u70b9\u7684\u540d\u5b57\uff0c\u9632\u6b62\u6811\u7684\u9ad8\u5ea6\u8fc7\u9ad8', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chanpinxian', to='CMDB.YewuTreeMptt'),
        ),
    ]
