# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-12-14 07:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultant_app', '0004_auto_20161209_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='to_do_list',
            name='text',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]