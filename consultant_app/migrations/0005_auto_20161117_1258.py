# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-11-17 12:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultant_app', '0004_auto_20161117_0743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 17, 12, 58, 58, 943487)),
        ),
        migrations.AlterField(
            model_name='project',
            name='assigned_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 17, 12, 58, 58, 937118)),
        ),
        migrations.AlterField(
            model_name='project',
            name='completion_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 17, 12, 58, 58, 937144)),
        ),
    ]
