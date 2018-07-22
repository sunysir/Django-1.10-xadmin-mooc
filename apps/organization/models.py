from datetime import datetime

from django.db import models

# Create your models here.
from course.models import Course

class CityDict(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'城市名')
    detail = models.TextField(verbose_name=u'城市简介')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name


class CourseOrg(models.Model):
    course = models.ForeignKey(Course)
    name = models.CharField(max_length=100, verbose_name=u'机构名')
    detail = models.TextField(verbose_name=u'机构简介')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    image = models.ImageField(upload_to='org/%Y%m', verbose_name=u'机构封面')
    fav_num = models.IntegerField(default=0, verbose_name=u'收藏数')
    adress = models.CharField(max_length=100, verbose_name=u'机构地址')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    city = models.ForeignKey(CityDict)

    class Meta:
        verbose_name = u'机构'
        verbose_name_plural = verbose_name


class Teacher(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name=u'所属机构')
    name = models.CharField(max_length=30, verbose_name=u'教师名')
    work_time = models.IntegerField(default=0, verbose_name=u'工龄')
    work_org = models.CharField(max_length=100, verbose_name=u'就职公司')
    age = models.IntegerField(default=0)
    work_postion = models.CharField(max_length=100, verbose_name=u'工作职位')
    classical_programs = models.CharField(max_length=100, verbose_name=u'经典课程')
    characteristic = models.CharField(max_length=100, verbose_name=u'授课特点')
    image = models.ImageField(upload_to='teacher/%Y%m', verbose_name=u'头像')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_num = models.IntegerField(default=0, verbose_name=u'收藏数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'教师'
        verbose_name_plural = verbose_name