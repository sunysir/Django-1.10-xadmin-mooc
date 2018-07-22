# _*_ encoding: utf-8 _*_
from captcha.fields import CaptchaField

from users.models import UserProfile

__author__ = 'suny'
__date__ = '2018/7/21 14:21'
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    captcha = CaptchaField()


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField()


class ResetPwdForm(forms.Form):
    password = forms.CharField(required=True)
    password2 = forms.CharField(required=True)







