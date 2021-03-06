# _*_ encoding: utf-8 _*_
from django.contrib.auth.decorators import login_required

__author__ = 'suny'
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)