# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-12-06 10:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultant_app', '0013_auto_20161206_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[(b'supporter', b'SUPPORTER'), (b'consultant', b'CONSULTANT')], max_length=15, null=True),
        ),
    ]