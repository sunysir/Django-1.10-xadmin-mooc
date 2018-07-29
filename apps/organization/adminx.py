# _*_ encoding: utf-8 _*_
import xadmin
from organization.models import Teacher,CityDict,CourseOrg

__author__ = 'suny'
__date__ = '2018/7/20 18:18'


class TeacherAdmin(object):
    list_display = ['course_org', 'name', 'work_time', 'work_org', 'age', 'work_postion', 'classical_programs', 'characteristic', 'click_nums', 'fav_num', 'add_time']
    list_filter = ['course_org', 'name', 'work_time', 'work_org', 'age', 'work_postion', 'classical_programs', 'characteristic', 'click_nums', 'fav_num', 'add_time']
    search_fields = ['course_org', 'name', 'work_time', 'work_org', 'age', 'work_postion', 'classical_programs', 'characteristic', 'click_nums', 'fav_num']


class CityDictAdmin(object):
    list_display = ['name', 'detail', 'add_time']
    list_filter = ['name', 'detail', 'add_time']
    search_fields = ['name', 'detail']


class CourseOrgAdmin(object):
    list_display = ['name', 'detail', 'click_nums', 'fav_num', 'adress', 'add_time', 'city']
    list_filter = ['name', 'detail', 'click_nums', 'fav_num', 'adress', 'add_time', 'city']
    search_fields = ['name', 'detail', 'click_nums', 'fav_num', 'adress', 'city']


xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
