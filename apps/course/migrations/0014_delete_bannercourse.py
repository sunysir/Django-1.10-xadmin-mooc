# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-07-28 20:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0013_bannercourse'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BannerCourse',
        ),
    ]
