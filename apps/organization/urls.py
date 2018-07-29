# _*_ encoding: utf-8 _*_
from organization.views import OrgListView, AskUserView, OrgDetailHomeView, OrgDetailTeacherView, OrgDetailCourseView, \
    OrgDetailDescView, UserFavView

__author__ = 'suny'

from django.conf.urls import url, include

app_name = 'org'
urlpatterns = [
    url(r'list/$', OrgListView.as_view(), name='org_list'),
    url(r'add_ask/$', AskUserView.as_view(), name='add_ask'),
    url(r'org_detail_home/(?P<org_id>[0-9])/', OrgDetailHomeView.as_view(), name='org_detail_home'),
    url(r'org_detail_teacher/(?P<org_id>[0-9])/', OrgDetailTeacherView.as_view(), name='org_detail_teacher'),
    url(r'org_detail_course/(?P<org_id>[0-9])/', OrgDetailCourseView.as_view(), name='org_detail_course'),
    url(r'org_detail_desc/(?P<org_id>[0-9])/', OrgDetailDescView.as_view(), name='org_detail_desc'),
    url(r'add_fav/', UserFavView.as_view(), name='add_fav'),
]