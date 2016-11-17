# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-11-16 13:44
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=500)),
                ('created_time', models.DateTimeField(default=datetime.datetime(2016, 11, 16, 13, 44, 22, 871992))),
            ],
        ),
        migrations.CreateModel(
            name='Consultant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(choices=[('active', 'active'), ('less_active', 'less_active'), ('independent', 'independent')], max_length=1)),
                ('skype_username', models.CharField(blank=True, max_length=100, null=True)),
                ('mobile_no', models.IntegerField(blank=True, max_length=25, null=True)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('experience', models.DurationField(blank=True, max_length=20, null=True)),
                ('curr_loc', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_title', models.CharField(blank=True, max_length=100, null=True)),
                ('project_description', models.TextField(max_length=1000)),
                ('assigned_date', models.DateTimeField(default=datetime.datetime(2016, 11, 16, 13, 44, 22, 865718))),
                ('completion_date', models.DateTimeField(default=datetime.datetime(2016, 11, 16, 13, 44, 22, 865752))),
            ],
        ),
        migrations.CreateModel(
            name='Supporter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('skype_username', models.CharField(blank=True, max_length=100, null=True)),
                ('mobile_no', models.IntegerField(blank=True, max_length=25, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='consultant',
            name='project_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='consultant_app.Project'),
        ),
        migrations.AddField(
            model_name='consultant',
            name='recruiter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recruits', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='consultant',
            name='supporter_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consultant_app.Supporter'),
        ),
        migrations.AddField(
            model_name='consultant',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='project_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consultant_app.Project'),
        ),
        migrations.AddField(
            model_name='comment',
            name='supporter_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consultant_app.Supporter'),
        ),
    ]
