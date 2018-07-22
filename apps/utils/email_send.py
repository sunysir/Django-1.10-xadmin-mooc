# _*_ encoding: utf-8 _*_
import random

from django.core.mail import send_mail

from mooc.settings import EMAIL_HOST_USER
from users.models import EmailVerifyRecord

__author__ = 'suny'
__date__ = '2018/7/21 17:09'


def generate_hash_code(MAX_LENTH=8):
    code = ''
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    length = len(chars) - 1
    for i in range(MAX_LENTH):
        code += chars[random.randint(0, length)]
    return code


def send_register_email(email, send_type):
    email_verify = EmailVerifyRecord()
    email_verify.email = email
    email_verify.code = generate_hash_code()
    email_verify.send_type = send_type
    email_verify.save()

    title = ''
    body = ''
    if send_type == 'register':
        title = '欢迎注册慕课在线网'
        body = '请点击链接完成注册 http://127.0.0.1:8000/active/{0}'.format(email_verify.code)
        email_status = send_mail(title, body, EMAIL_HOST_USER, [email])

    if send_type == 'forget':
        title = '慕课网密码重置'
        body = '请点击链接完成注册 http://127.0.0.1:8000/reset/{0}'.format(email_verify.code)
        email_status = send_mail(title, body, EMAIL_HOST_USER, [email])

    if email_status:
        pass


