# _*_ encoding:utf-8 _*_
from datetime import datetime

from django.db import models

# Create your models here.
from organization.models import CourseOrg, Teacher


class Course(models.Model):
    teacher = models.ForeignKey(Teacher, verbose_name=u'授课老师', null=True, blank=True)
    is_banner = models.BooleanField(default=False)
    org = models.ForeignKey(CourseOrg, verbose_name=u'课程机构', null=True, blank=True)
    course_know = models.CharField(max_length=100, verbose_name=u'课程须知', null=True, blank=True)
    teacher_enlighten = models.CharField(max_length=100, verbose_name=u'老师指点', null=True, blank=True)
    name = models.CharField(max_length=100,verbose_name=u'课程名')
    abstract = models.CharField(max_length=500, verbose_name=u'课程简介')
    detail = models.TextField(verbose_name=u'课程详情')
    degree = models.CharField(choices=(('easy', u'简单'), ('medium', u'中等'), ('difficulty', u'困难')), default='easy', verbose_name='课程难度', max_length=30)
    period = models.IntegerField(default=0,verbose_name=u'课时(按分钟计)')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    tag = models.CharField(max_length=10, verbose_name=u'课程标签',null=True,blank=True)
    image = models.ImageField(upload_to='course/%Y/%m', verbose_name=u'封面图', max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name=u'课程点击数')
    category = models.CharField(max_length=20, verbose_name=u'课程类别',null=True,blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def get_chapter_nums(self):
        chaper_nums = self.lesson_set.all().count()
        return chaper_nums

    def get_user_nums(self):
        user_nums = self.usercourse_set.all()[:5]
        return user_nums

    def __str__(self):
        return self.name


class BannerCourse(Course):

    class Meta:
        verbose_name = u'轮播课程'
        verbose_name_plural = verbose_name
        proxy = True


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程名')
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程章节'
        verbose_name_plural = verbose_name

    def get_videos(self):
        videos = self.video_set.all()
        return videos

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节名')
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程名')
    name = models.CharField(max_length=100, verbose_name=u'资源名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    download = models.FileField(upload_to='course/resource/%Y%m', verbose_name=u'资源文件', max_length=100)

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
