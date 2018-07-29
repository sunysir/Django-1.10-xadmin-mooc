# _*_ encoding: utf-8 _*_
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from course.views import CourseListView, CourseDetailView, CourseLessonView, CourseCommentView, CourseAddCommentView, \
    CourseTeacherView, TeacherDetailView

__author__ = 'suny'

app_name = "course"
urlpatterns = [
    url(r'^course_list/', CourseListView.as_view(), name='course_list'),
    url(r'^course_detail/(?P<course_id>[0-9]*)/', CourseDetailView.as_view(), name='course_detail'),
    url(r'^course_lesson/(?P<course_id>[0-9]*)/', CourseLessonView.as_view(), name='course_lesson'),
    url(r'^course_comment/(?P<course_id>[0-9]*)/', CourseCommentView.as_view(), name='course_comment'),
    url(r'^add_comment/', CourseAddCommentView.as_view(), name='add_comment'),
    url(r'^course_teacher/', CourseTeacherView.as_view(), name='course_teacher'),
    url(r'^course_teacher_detail/(?P<teacher_id>[0-9]*)/', TeacherDetailView.as_view(), name='course_teacher_detail'),
]