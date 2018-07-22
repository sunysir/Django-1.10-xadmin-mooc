# _*_ encoding:utf-8 _*_
from datetime import datetime

from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=100,verbose_name=u'课程名')
    abstract = models.CharField(max_length=500, verbose_name=u'课程简介')
    detail = models.TextField(verbose_name=u'课程详情')
    degree = models.CharField(choices=(('easy', u'简单'), ('medium', u'中等'), ('difficulty', u'困难')), default='easy', verbose_name='课程难度', max_length=30)
    period = models.IntegerField(default=0,verbose_name=u'课时(按分钟计)')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to='course/%Y/%m', verbose_name=u'封面图', max_length=100)
    click_nums = models.ImageField(default=0, verbose_name=u'课程点击数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程名')
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程章节'
        verbose_name_plural = verbose_name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节名')
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节视频'
        verbose_name_plural = verbose_name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程名')
    name = models.CharField(max_length=100, verbose_name=u'资源名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    download = models.FileField(upload_to='course/resource/%Y%m', verbose_name=u'资源文件', max_length=100)

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name
