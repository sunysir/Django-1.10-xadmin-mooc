# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-07-19 09:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_banner_emailverifyrecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='index',
            field=models.IntegerField(verbose_name='图片序号'),
        ),
    ]