# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-07-23 12:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CityDict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='城市名')),
                ('detail', models.TextField(verbose_name='城市简介')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '城市',
                'verbose_name_plural': '城市',
            },
        ),
        migrations.CreateModel(
            name='CourseOrg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='机构名')),
                ('detail', models.TextField(verbose_name='机构简介')),
                ('click_nums', models.IntegerField(default=0, verbose_name='点击数')),
                ('image', models.ImageField(upload_to='org/%Y%m', verbose_name='机构封面')),
                ('fav_num', models.IntegerField(default=0, verbose_name='收藏数')),
                ('adress', models.CharField(max_length=100, verbose_name='机构地址')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.CityDict')),
            ],
            options={
                'verbose_name': '机构',
                'verbose_name_plural': '机构',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='教师名')),
                ('work_time', models.IntegerField(default=0, verbose_name='工龄')),
                ('work_org', models.CharField(max_length=100, verbose_name='就职公司')),
                ('age', models.IntegerField(default=0)),
                ('work_postion', models.CharField(max_length=100, verbose_name='工作职位')),
                ('classical_programs', models.CharField(max_length=100, verbose_name='经典课程')),
                ('characteristic', models.CharField(max_length=100, verbose_name='授课特点')),
                ('image', models.ImageField(upload_to='teacher/%Y%m', verbose_name='头像')),
                ('click_nums', models.IntegerField(default=0, verbose_name='点击数')),
                ('fav_num', models.IntegerField(default=0, verbose_name='收藏数')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('course_org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.CourseOrg', verbose_name='所属机构')),
            ],
            options={
                'verbose_name': '教师',
                'verbose_name_plural': '教师',
            },
        ),
    ]
