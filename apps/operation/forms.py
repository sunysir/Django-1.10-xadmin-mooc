# _*_ encoding: utf-8 _*_
__author__ = 'suny'
__date__ = '2018/7/24 10:06'
import re

from django import forms

from operation.models import UserAsk




class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course']

    #自定义表单字段验证
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = '^1[358]\d{9}$|^147\d{8}$|^176\d{8}$'
        r = re.compile(REGEX_MOBILE)
        if r.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u'手机号码错误', code='mobile_invalid')