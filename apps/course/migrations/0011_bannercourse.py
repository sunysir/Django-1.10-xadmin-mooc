# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-07-28 20:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0010_auto_20180728_2008'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannerCourse',
            fields=[
                ('course_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='course.Course')),
            ],
            options={
                'verbose_name': '轮播课程',
                'verbose_name_plural': '轮播课程',
            },
            bases=('course.course',),
        ),
    ]