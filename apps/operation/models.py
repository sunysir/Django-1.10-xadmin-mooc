from datetime import datetime

from django.db import models

# Create your models here.
from course.models import Course
from users.models import UserProfile


class UserAsk(models.Model):
    name = models.CharField(max_length=30, verbose_name=u'姓名')
    mobile = models.CharField(max_length=11, verbose_name=u'手机号')
    course = models.CharField(max_length=30, verbose_name=u'课程名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户咨询'
        verbose_name_plural = verbose_name


class UserComment(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程名')
    user = models.ForeignKey(UserProfile, verbose_name=u'用户名')
    comment = models.CharField(max_length=200, verbose_name=u'评论内容')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户评论'
        verbose_name_plural = verbose_name


class UserFav(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u'用户名')
    fav_id = models.IntegerField(default=0, verbose_name=u'数据id选择')
    fav_type = models.IntegerField(choices=((1, u'课程'), (2, u'机构'), (3, u'教师')), default=1 , verbose_name=u'种类选择')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户收藏'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    # id为0表示发送信息给所有用户
    user = models.IntegerField(default=0, verbose_name=u'用户id')
    send_time = models.DateTimeField(default=datetime.now, verbose_name=u'发送时间')
    has_read = models.BooleanField(default=False, verbose_name=u'是否已读')
    message = models.CharField(max_length=500, verbose_name=u'消息内容')

    class Meta:
        verbose_name = u'用户消息'
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程名')
    user = models.ForeignKey(UserProfile, verbose_name=u'用户名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户课程'
        verbose_name_plural = verbose_name

