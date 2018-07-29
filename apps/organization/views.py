
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from django.shortcuts import render_to_response

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from course.models import Course
from operation.forms import UserAskForm
from operation.models import UserFav
from organization.models import CityDict, CourseOrg, Teacher
from users.views import LoginView
from utils.mixin_utils import LoginRequiredMixin


class OrgListView(View):
    def get(self, request):
        nav = 'org'
        all_city = CityDict.objects.all()
        all_org = CourseOrg.objects.all()
        city_id = request.GET.get('city', '')
        category = request.GET.get('category', '')
        keywords = request.GET.get('keywords', '')
        if keywords:
            all_org = CourseOrg.objects.filter(Q(name__icontains=keywords)|Q(detail__icontains=keywords))
        user_ask_forms = UserAskForm()
        if category and not city_id:
            all_org = CourseOrg.objects.filter(category=category)
        if city_id and not category:
            all_org = CourseOrg.objects.filter(city_id=int(city_id))
        if category and city_id:
            all_org = CourseOrg.objects.filter(city_id=int(city_id), category=category)


        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # objects = ['john', 'edward', 'josh', 'frank']

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_org, 5, request=request)
        orgs = p.page(page)
        return render(request, 'org-list.html', {'all_city': all_city,
                                                 'all_org': orgs,
                                                 'city_id': city_id,
                                                 'category':category,
                                                 'user_ask_forms': user_ask_forms,
                                                 'nav': nav
                                                 })


class AskUserView(View):
    def post(self, request):
        forms = UserAskForm(request.POST)
        if forms.is_valid():
            forms.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加出错"}', content_type='application/json')


class OrgDetailHomeView(View):
    def get(self, request, org_id):
        has_fav = False
        left_flag = 'org_detail_home'
        org = CourseOrg.objects.get(id=org_id)
        org.click_nums+=1
        org.save()
        courses = Course.objects.filter(org_id=int(org_id))[:3]
        # teachers = Teacher.objects.filter(course_org__teacher=int(org_id))
        #另一种逻辑方法
        course_org = CourseOrg.objects.get(id=int(org_id))
        if request.user.is_authenticated():
            if UserFav.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
            else:
                has_fav = False
        teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {'left_flag': left_flag, 'course_org': course_org, 'courses': courses, 'org_id': org_id, 'teachers': teachers, 'has_fav': has_fav})


class OrgDetailTeacherView(View):
    def get(self, request, org_id):
        has_fav = False
        left_flag = 'org_detail_teacher'
        courses = Course.objects.filter(org_id=int(org_id))[:3]
        # teachers = Teacher.objects.filter(course_org__teacher=int(org_id))
        # 另一种逻辑方法
        course_org = CourseOrg.objects.get(id=int(org_id))
        teachers = course_org.teacher_set.all()
        if request.user.is_authenticated():
            if UserFav.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
            else:
                has_fav = False
        return render(request, 'org-detail-teachers.html', {'left_flag': left_flag, 'course_org': course_org, 'courses': courses, 'org_id': org_id, 'teachers': teachers, 'has_fav': has_fav})


class OrgDetailCourseView(View):
    def get(self, request, org_id):
        has_fav = False
        left_flag = 'org_detail_course'
        courses = Course.objects.filter(org_id=int(org_id))
        # teachers = Teacher.objects.filter(course_org__teacher=int(org_id))
        # 另一种逻辑方法
        course_org = CourseOrg.objects.get(id=int(org_id))
        teachers = course_org.teacher_set.all()
        if request.user.is_authenticated():
            if UserFav.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
            else:
                has_fav = False
        return render(request, 'org-detail-course.html', {'left_flag': left_flag, 'course_org': course_org, 'courses': courses, 'org_id': org_id, 'teachers': teachers, 'has_fav': has_fav})


class OrgDetailDescView(View):
    def get(self, request, org_id):
        has_fav = False
        left_flag = 'org_detail_desc'
        courses = Course.objects.filter(org_id=int(org_id))[:3]
        # teachers = Teacher.objects.filter(course_org__teacher=int(org_id))
        # 另一种逻辑方法
        course_org = CourseOrg.objects.get(id=int(org_id))
        teachers = course_org.teacher_set.all()[:1]
        if request.user.is_authenticated():
            if UserFav.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
            else:
                has_fav = False
        return render(request, 'org-detail-desc.html', {'left_flag': left_flag, 'course_org': course_org, 'courses': courses, 'org_id': org_id, 'teachers': teachers, 'has_fav': has_fav})


class UserFavView(View):
    def post(self, request):
            has_fav = False
            fav_id = request.POST.get('fav_id', 0)
            fav_type = request.POST.get('fav_type', 0)
            if request.user.is_authenticated():
                if request.user.is_authenticated():
                    record_exist = UserFav.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
                    if record_exist:
                        record_exist.delete()
                        if int(fav_type) == 1:
                            course = Course.objects.get(fav_id=int(fav_id))
                            course.fav_nums-=1
                            course.save()
                        elif int(fav_type) == 2:
                            org = CourseOrg.objects.get(fav_id=int(fav_id))
                            org.fav_nums -= 1
                            org.save()
                        else:
                            teacher = Teacher.objects.get(fav_id=int(fav_id))
                            teacher.fav_nums -= 1
                            teacher.save()
                        return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')
                    else:
                        user_fav = UserFav()
                        user_fav.user = request.user
                        user_fav.fav_id = int(fav_id)
                        user_fav.fav_type = int(fav_type)
                        user_fav.save()
                        if int(fav_type) == 1:
                            course = Course.objects.get(fav_id=int(fav_id))
                            course.fav_nums+=1
                            course.save()
                        elif int(fav_type) == 2:
                            org = CourseOrg.objects.get(fav_id=int(fav_id))
                            org.fav_nums += 1
                            org.save()
                        else:
                            teacher = Teacher.objects.get(fav_id=int(fav_id))
                            teacher.fav_nums += 1
                            teacher.save()
                        return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
