# _*_ encoding: utf-8 _*_
from captcha.fields import CaptchaField

from users.models import UserProfile

__author__ = 'suny'
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


class ModifyPwdForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['password']


class ModifyEmailForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birthday', 'gender', 'adress', 'mobile']


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']





