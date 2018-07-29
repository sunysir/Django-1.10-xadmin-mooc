# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-07-24 15:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_courseorg_category'),
        ('course', '0002_auto_20180724_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='org',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.CourseOrg', verbose_name='课程机构'),
        ),
    ]
