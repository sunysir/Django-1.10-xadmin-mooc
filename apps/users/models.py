# _*_ encoding:utf-8 _*_
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models import Q


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u'昵称', default=u'')
    birthday = models.DateField(verbose_name=u'生日', null=True, blank=True)
    gender = models.CharField(choices=(('male', u'男'), ('female', u'女')), default=u'male', max_length=6)
    adress = models.CharField(verbose_name=u'地址', default=u'',max_length=100)
    mobile = models.CharField(verbose_name=u'电话', max_length=11)
    image = models.ImageField(upload_to='image/%Y/%m', default='image/default.png',max_length=100)

    def get_user_unread_message_nums(self):
        from operation.models import UserMessage
        usermessage = UserMessage.objects.filter(user=self.id, has_read=False).count()
        return usermessage

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u'验证码')
    email = models.EmailField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(choices=(('forget', u'忘记密码'), ('register', u'注册'), ('modify', u'更换邮箱')), max_length=20, verbose_name=u'发送类型')
    send_time= models.DateTimeField(verbose_name=u'发送时间', default=datetime.now)

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name

class Banner(models.Model):
    titile = models.CharField(max_length=30, verbose_name=u'标题')
    image= models.ImageField(upload_to='image/%Y/%m', verbose_name=u'轮播图图片')
    url = models.URLField(verbose_name=u'访问地址')
    index = models.IntegerField(verbose_name=u'图片序号')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = u'轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.titile
