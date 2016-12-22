# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-12-08 16:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('consultant_app', '0002_auto_20161207_0545'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='sender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Notification', to=settings.AUTH_USER_MODEL),
        ),
    ]
