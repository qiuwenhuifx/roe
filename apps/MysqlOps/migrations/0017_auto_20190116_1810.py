# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-01-16 10:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MysqlOps', '0016_auto_20190116_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='mysql_sql_log',
            name='affect_row',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='mysql_sql_log',
            name='exe_status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
