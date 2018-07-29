import json

from django.core.mail import send_mail
from django.core.paginator import PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from pure_pagination import Paginator

from course.models import Course
from operation.models import UserCourse, UserFav, UserMessage
from organization.models import CourseOrg, Teacher
from users.forms import LoginForm, RegisterForm, ForgetPwdForm, ResetPwdForm, UserInfoForm, UploadImageForm, \
    ModifyPwdForm, ModifyEmailForm
from users.models import UserProfile, EmailVerifyRecord, Banner
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin


#增添邮箱注册
class CustomBackends(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as ex:
            return None


#慕课网首页视图类
class IndexView(View):
    def get(self, request):
        nav = ''
        all_orgs = CourseOrg.objects.all()
        courses = Course.objects.all()[:6]
        banner_course = Course.objects.filter(is_banner=True)
        banners = Banner.objects.all()
        return render(request, 'index.html', {'nav': nav, 'courses': courses, 'all_orgs': all_orgs, 'banner_course': banner_course, 'banners': banners})


#用户登陆视图类
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', "")
            pass_word = request.POST.get('password', "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'forms': login_form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


# 原生登陆代码
# def user_login(request):
#     if request.method == 'POST':
#         user_name = request.POST.get('username', "")
#         pass_word = request.POST.get('password', "")
#         user = authenticate(username=user_name, password=pass_word)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 return render(request, 'index.html')
#             else:
#                 return render(request, 'login.html', {'msg': '用户未激活'})
#         else:
#             return render(request, 'login.html', {'msg': '用户名或密码错误'})
#     else:
#         return render(request, 'login.html', {})


#用户激活视图类
class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
            return render(request, 'login.html')
        else:
            return render(request, 'invaild.html')


#用户注册视图类
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            pass_word = request.POST.get('password', '')
            all_records = UserProfile.objects.filter(username=user_name)
            if all_records:
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已存在'})
            else:
                user_profile = UserProfile()
                user_profile.username = user_name
                user_profile.email = user_name
                user_profile.password = make_password(pass_word)
                user_profile.is_active = False
                usermessage = UserMessage()
                usermessage.user = user_profile.id
                usermessage.message = '欢迎注册慕学在线网'
                usermessage.save()
                user_profile.save()
                send_register_email(user_name, 'register')
                return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


#忘记密码视图类
class ForgetPwdView(View):
    def get(self, request):
        forms = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forms': forms})

    def post(self, request):
        forms = ForgetPwdForm(request.POST)
        if forms.is_valid():
            email = request.POST.get('email', '')
            all_records = UserProfile.objects.filter(email=email)
            if all_records:
                send_register_email(email, 'forget')
                return render(request, 'send_success.html')
            else:
                register_form = RegisterForm()
                return render(request, 'register.html', {'register_form': register_form, 'msg': '该用户不存在请注册'})
        else:
            register_form = RegisterForm()
            return render(request, 'forgetpwd.html', {'register_form': register_form, 'msg': '请输入正确邮箱'})


#重置密码视图类
class ResetPwdView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'invaild.html')


#忘记密码找回判断视图类
class ModifyView(View):
    def post(self, request):
        forms = ResetPwdForm(request.POST)
        if forms.is_valid():
            pwd1 = request.POST.get('password', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'msg': '两次密码输入不一致'})
            else:
                users = UserProfile.objects.filter(email=email)
                if users:
                    for user in users:
                        user.password = make_password(pwd1)
                        user.save()
                return render(request, 'modify_success.html')
        else:
            return render(request, 'password_reset.html')


#用户个人信息视图类
class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        fav_tag = 'UserInfo'
        userInfo_form = UserInfoForm()
        return render(request, 'usercenter-info.html', {'userInfo_form': userInfo_form, 'fav_tag': fav_tag})

    def post(self, request):
        userInfo_form = UserInfoForm(request.POST, instance=request.user)
        if userInfo_form.is_valid():
            userInfo_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"failure"}', content_type='application/json')


#用户修改头像视图类
class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        upload_image = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if upload_image.is_valid():
            upload_image.save(commit=True)
            return render(request, 'usercenter-info.html')


#用户修改密码视图类
class ResetPwView(LoginRequiredMixin, View):
    def post(self, request):
        reset_pw_form = ModifyPwdForm(request.POST, instance=request.user)
        if reset_pw_form.is_valid():
            pw1 = request.POST.get('password')
            pw2 = request.POST.get('password2')
            if pw1 != pw2:
                return HttpResponse('{"status":"fail","msg":"两次密码出入不一致"}', content_type='application/json')
            elif len(pw1) < 6 or len(pw2) < 6:
                return HttpResponse('{"status":"fail","msg":"密码长度最少6位"}', content_type='application/json')
            elif len(pw1) > 20 or len(pw2) > 20:
                return HttpResponse('{"status":"fail","msg":"密码长度最大20位"}', content_type='application/json')
            else:
                reset_pw_form.save(commit=True)
                return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(reset_pw_form.errors), content_type='application/json')


#用户修改邮箱视图类
class ModifyEmailView(LoginRequiredMixin, View):
    def get(self, request):
        new_email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=new_email):
            return HttpResponse('{"status":"failure","email":"邮箱已经注册"}', content_type='application/json')
        status = send_register_email(new_email, 'modify')
        if status:
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"failure"}', content_type='application/json')

    def post(self, request):
        if EmailVerifyRecord.objects.filter(code=request.POST.get('code'),email=request.POST.get('email'),send_type='modify'):
            email_form = ModifyEmailForm(request.POST, instance=request.user)
            if email_form.is_valid():
                email_form.save(commit=True)
                return HttpResponse('{"status":"success"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"failure"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"failure"}', content_type='application/json')


#用户课程视图类
class UserMyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        fav_tag = 'UserMyCourse'
        all_usercourse = UserCourse.objects.filter(user=request.user)
        all_courses = [usercourse.course for usercourse in all_usercourse]
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # objects = ['john', 'edward', 'josh', 'frank']

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_courses, 8, request=request)
        all_courses = p.page(page)
        return render(request, 'usercenter-mycourse.html', {'all_courses': all_courses, 'fav_tag': fav_tag})


#用户消息视图类
class UserMyMessageView(LoginRequiredMixin, View):
    def get(self, request):
        fav_tag = 'UserMyMessage'
        user_id = request.user.id
        all_user_messages = UserMessage.objects.filter(user=user_id)
        all_user_unread_messages = UserMessage.objects.filter(user=user_id, has_read=False )
        for user_message in all_user_unread_messages:
            user_message.has_read = True
            user_message.save()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

            # objects = ['john', 'edward', 'josh', 'frank']

            # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_user_messages, 8, request=request)
        all_user_messages = p.page(page)
        return render(request, 'usercenter-message.html', {'all_user_messages': all_user_messages, 'fav_tag': fav_tag})


#用户收藏机构视图类
class UserMyFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        fav_tag = 'UserMyFav'
        all_userfavs = UserFav.objects.filter(fav_type=2)
        all_org_ids = [userfav.fav_id for userfav in all_userfavs]
        all_orgs = CourseOrg.objects.filter(id__in=all_org_ids)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # objects = ['john', 'edward', 'josh', 'frank']

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_orgs, 8, request=request)
        all_orgs = p.page(page)
        return render(request, 'usercenter-fav-org.html', {'all_orgs': all_orgs, 'fav_tag': fav_tag})


#用户收藏老师视图类
class UserMyFavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        fav_tag = 'UserMyFav'
        all_userfavs = UserFav.objects.filter(fav_type=3)
        all_teacher_ids = [userfav.fav_id for userfav in all_userfavs]
        all_teachers = Teacher.objects.filter(id__in=all_teacher_ids)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # objects = ['john', 'edward', 'josh', 'frank']

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_teachers, 8, request=request)
        all_teachers = p.page(page)
        return render(request, 'usercenter-fav-teacher.html', {'all_teachers': all_teachers, 'fav_tag': fav_tag})


#用户收藏课程视图类
class UserMyFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        fav_tag = 'UserMyFav'
        all_userfavs = UserFav.objects.filter(fav_type=1)
        all_course_ids = [userfav.fav_id for userfav in all_userfavs]
        all_courses = Course.objects.filter(id__in=all_course_ids)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # objects = ['john', 'edward', 'josh', 'frank']

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_courses, 8, request=request)
        all_courses = p.page(page)
        return render(request, 'usercenter-fav-course.html', {'all_courses': all_courses, 'fav_tag': fav_tag})


def page_not_found_404(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_not_found_500(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response