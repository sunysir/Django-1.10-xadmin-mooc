# _*_ encoding: utf-8 _*_
import xadmin
from course.models import Course, Lesson, Video, CourseResource

__author__ = 'suny'
class LessonInline(object):
    model = Lesson
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'degree', 'period']
    list_filter = ['name', 'degree', 'period']
    search_fields = ['name', 'degree', 'period']
    inlines = [LessonInline]
    readonly_fields = ['fav_nums', 'click_nums', 'students']

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

class BannerCourseAdmin(object):
    list_display = ['name', 'degree', 'period']
    list_filter = ['name', 'degree', 'period']
    search_fields = ['name', 'degree', 'period']
    inlines = [LessonInline]
    readonly_fields = ['fav_nums', 'click_nums', 'students']

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs

xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson)
xadmin.site.register(Video)
xadmin.site.register(CourseResource)
# xadmin.site.register(BannerCourse, BannerCourseAdmin)