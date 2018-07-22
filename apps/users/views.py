from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from users.forms import LoginForm, RegisterForm, ForgetPwdForm, ResetPwdForm
from users.models import UserProfile, EmailVerifyRecord
from utils.email_send import send_register_email


class CustomBackends(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as ex:
            return None


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
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'forms': login_form})

#原生登陆代码
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
                user_profile.save()
                send_register_email(user_name, 'register')
                return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


class ForgetPwdView(View):
    def get(self, request):
        forms = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forms': forms})

    def post(self, request):
        forms = ForgetPwdForm(request.POST)
        if forms.is_valid():
            email = request.POST.get('email','')
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


class ResetPwdView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'invaild.html')


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


