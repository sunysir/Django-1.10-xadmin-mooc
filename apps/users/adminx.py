# _*_ encoding: utf-8 _*_
import xadmin
from users.models import Banner, EmailVerifyRecord
from xadmin import views

__author__ = 'suny'
__date__ = '2018/7/20 16:27'


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = '慕学在线后台管理系统'
    site_footer = '慕学在线网'
    menu_style = 'accordion'


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']


class BannerAdmin(object):
    list_display = ['titile', 'image', 'url', 'index', 'add_time']
    list_filter = ['titile', 'image', 'url', 'index', 'add_time']
    search_fields = ['titile', 'image', 'url', 'index']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
