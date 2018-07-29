# _*_ encoding: utf-8 _*_
from users.views import UserInfoView, UserMyCourseView, UserMyMessageView, UploadImageView, ResetPwView, \
    ModifyEmailView, UserMyFavOrgView, UserMyFavCourseView, UserMyFavTeacherView

__author__ = 'suny'
from django.conf.urls import url

app_name = 'users'
urlpatterns = [
    url(r'userInfo/$', UserInfoView.as_view(), name='userInfo'),
    url(r'userMyCourse/$', UserMyCourseView.as_view(), name='userMyCourse'),
    url(r'userMyFavOrg/$', UserMyFavOrgView.as_view(), name='userMyFavOrg'),
    url(r'userMyFavCourse/$', UserMyFavCourseView.as_view(), name='userMyFavCourse'),
    url(r'userMyFavTeacher/$', UserMyFavTeacherView.as_view(), name='userMyFavTeacher'),
    url(r'userMessage/$', UserMyMessageView.as_view(), name='userMessage'),
    url(r'uploadImage/$', UploadImageView.as_view(), name='uploadImage'),
    url(r'resetPw/$', ResetPwView.as_view(), name='resetPw'),
    url(r'modifyEmail/$', ModifyEmailView.as_view(), name='modifyEmail'),

]

