# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-07-25 20:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_course_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_know',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='课程须知'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher_enlighten',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='老师指点'),
        ),
    ]
