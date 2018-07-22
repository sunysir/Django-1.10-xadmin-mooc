# _*_ encoding: utf-8 _*_
import xadmin
from course.models import Course, Lesson, Video, CourseResource

__author__ = 'suny'
__date__ = '2018/7/20 18:34'


xadmin.site.register(Course)
xadmin.site.register(Lesson)
xadmin.site.register(Video)
xadmin.site.register(CourseResource)