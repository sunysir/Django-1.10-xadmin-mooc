# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-07-28 20:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0003_usercomment_add_time'),
        ('course', '0011_bannercourse'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bannercourse',
            name='course_ptr',
        ),
        migrations.DeleteModel(
            name='BannerCourse',
        ),
    ]
