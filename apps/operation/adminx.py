# _*_ encoding: utf-8 _*_
import xadmin
from operation.models import UserAsk, UserComment, UserFav, UserMessage, UserCourse

__author__ = 'suny'
__date__ = '2018/7/20 18:30'


class UserAskAdmin(object):
    list_display = ['name', 'detail', 'add_time']
    list_filter = ['name', 'detail', 'add_time']
    search_fields = ['name', 'detail']


class UserFavAdmin(object):
    list_display = ['name', 'detail', 'add_time']
    list_filter = ['name', 'detail', 'add_time']
    search_fields = ['name', 'detail']


class UserMessageAdmin(object):
    list_display = ['name', 'detail', 'add_time']
    list_filter = ['name', 'detail', 'add_time']
    search_fields = ['name', 'detail']


class CityDictAdmin(object):
    list_display = ['name', 'detail', 'add_time']
    list_filter = ['name', 'detail', 'add_time']
    search_fields = ['name', 'detail']


class UserCourseAdmin(object):
    list_display = ['name', 'detail', 'add_time']
    list_filter = ['name', 'detail', 'add_time']
    search_fields = ['name', 'detail']


xadmin.site.register(UserAsk)
xadmin.site.register(UserComment)
xadmin.site.register(UserFav)
xadmin.site.register(UserMessage)
xadmin.site.register(UserCourse)