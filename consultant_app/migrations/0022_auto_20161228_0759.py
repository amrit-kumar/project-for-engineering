# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-12-28 07:59
from __future__ import unicode_literals

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('consultant_app', '0021_auto_20161228_0758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image_ppoi',
            field=versatileimagefield.fields.PPOIField(default='0.5x0.5', editable=False, max_length=20),
        ),
    ]