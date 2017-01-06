# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-11-30 07:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('consultant_app', '0007_skillset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skillset',
            name='technology',
            field=models.ForeignKey(blank=True, max_length=30, null=True, on_delete=django.db.models.deletion.CASCADE, to='consultant_app.Technology'),
        ),
    ]
