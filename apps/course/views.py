# _*_ encoding: utf-8 _*_
from django.core.paginator import PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from pure_pagination import Paginator

from course.models import Course, Lesson, CourseResource
from operation.models import UserFav, UserComment, UserCourse
from organization.models import Teacher
from utils.mixin_utils import LoginRequiredMixin
from django.db.models import Q


class CourseListView(View):
    def get(self, request):
        nav = 'course'
        all_course = Course.objects.all().order_by('-add_time')
        keywords = request.GET.get('keywords', "")
        if keywords:
            all_course = Course.objects.filter(Q(name__icontains=keywords)|Q(detail__icontains=keywords)|Q(abstract__icontains=keywords))
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_course = all_course.order_by('-students')
            if sort == 'hot':
                all_course = all_course.order_by('-click_nums')
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # objects = ['john', 'edward', 'josh', 'frank']

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_course, 6, request=request)
        all_course = p.page(page)
        return render(request, 'course-list.html', {'nav': nav, 'hot_courses':hot_courses, 'sort':sort, 'all_course': all_course})


class CourseDetailView(View):
    def get(self, request, course_id):
        nav = 'course'
        has_fav_course = False
        has_fav_org = False
        course = Course.objects.get(id=int(course_id))
        course.click_nums+=1
        course.save()
        relate_courses = list(Course.objects.filter(tag=course.tag)[:3])
        if request.user.is_authenticated():
            if course in relate_courses:
                relate_courses.remove(course)
            if UserFav.objects.filter(user=request.user, fav_type=2, fav_id=course.org_id):
                has_fav_org = True
            if UserFav.objects.filter(user=request.user, fav_type=1, fav_id=course.id):
                has_fav_course = True

        return render(request, 'course-detail.html', {'nav': nav,
                                                      'course': course,
                                                      'course_id':course_id,
                                                      'relate_courses': relate_courses,
                                                      'has_fav_org': has_fav_org,
                                                      'has_fav_course': has_fav_course
                                                      })


class CourseLessonView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        nav = 'course'
        current_course = Course.objects.get(id=int(course_id))
        res_exist = UserCourse.objects.filter(user=request.user, course=current_course)
        if not res_exist:
            user_course = UserCourse(user=request.user, course=current_course)
            user_course.save()
        all_lessons = Lesson.objects.filter(course_id=int(course_id))
        all_resource = CourseResource.objects.filter(course_id=course_id)
        all_usercourse = UserCourse.objects.filter(course_id=course_id)
        user_ids = [usercourse.user_id for usercourse in all_usercourse]
        all_usercourses = UserCourse.objects.filter(user_id__in=user_ids)
        temp_courses_id = list(set([usercourse.course_id for usercourse in all_usercourses]))
        relate_courses = Course.objects.filter(id__in=temp_courses_id).order_by('-click_nums')[:3]
        return render(request, 'course-video.html', {'nav': nav,
                                                     'all_lessons': all_lessons,
                                                     'course_id': course_id,
                                                     'current_course': current_course,
                                                     'all_resource': all_resource,
                                                     'relate_courses': relate_courses
                                                     })


class CourseCommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        nav = 'course'
        current_course = Course.objects.get(id=int(course_id))
        all_resource = CourseResource.objects.filter(course_id=course_id)
        all_comments = UserComment.objects.all()
        all_usercourse = UserCourse.objects.filter(course_id=course_id)
        user_ids = [usercourse.user_id for usercourse in all_usercourse]
        all_usercourses = UserCourse.objects.filter(user_id__in=user_ids)
        temp_courses_id = list(set([usercourse.course_id for usercourse in all_usercourses]))
        relate_courses = Course.objects.filter(id__in=temp_courses_id).order_by('-click_nums')[:3]
        return render(request, 'course-comment.html', {'nav': nav,
                                                       'course_id': course_id,
                                                       'current_course': current_course,
                                                       'all_resource': all_resource, 'all_comments': all_comments,
                                                       'relate_courses': relate_courses
                                                       })


class CourseAddCommentView(View):
    def post(self, request):
        if request.user.is_authenticated:
            user_comment = UserComment()
            user_comment.user = request.user
            course = Course.objects.get(id=int(request.POST.get('course_id', 0)))
            user_comment.course = course
            user_comment.comment = request.POST.get('comments', "")
            user_comment.save()
            return HttpResponse('{"status":"success","msg":"评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')


class CourseTeacherView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()
        nav = 'teacher'
        sort = request.GET.get('sort')
        teacher_nums = Teacher.objects.all().count()
        hot_teachers = Teacher.objects.all().order_by('-click_nums')[:3]
        keywords = request.GET.get('keywords', '')
        if keywords:
            all_teachers = Teacher.objects.filter(Q(name__icontains=keywords)|Q(work_postion__icontains=keywords))
        if sort == 'hot':
            all_teachers = all_teachers.order_by('-click_nums')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # objects = ['john', 'edward', 'josh', 'frank']

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_teachers, 5, request=request)
        all_teachers = p.page(page)
        return render(request, 'teachers-list.html', {'nav': nav,
                                                      'all_teachers': all_teachers,
                                                      'sort': sort,
                                                      'hot_teachers': hot_teachers,
                                                      'teacher_nums': teacher_nums
                                                      }
                      )


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        nav = 'teacher'
        has_fav_teacher = False
        has_fav_org = False
        hot_teachers = Teacher.objects.all().order_by('-click_nums')[:3]
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums+=1
        teacher.save()
        all_course = Course.objects.filter(teacher=teacher)
        res_exist_teacher = UserFav.objects.filter(user=request.user, fav_id=int(teacher_id), fav_type=3)
        res_exist_org = UserFav.objects.filter(user=request.user, fav_id=int(teacher.course_org.id), fav_type=2)
        if res_exist_teacher:
            has_fav_teacher = True
        if res_exist_org:
            has_fav_org = True
        return render(request, 'teacher-detail.html', {'nav': nav, 'hot_teachers': hot_teachers, 'teacher': teacher, 'all_course': all_course, 'has_fav_teacher': has_fav_teacher, 'has_fav_org': has_fav_org})