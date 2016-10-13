# -*- coding: utf-8 -*-

from django.shortcuts import render
import datetime
from zqb_user.functions import SendMobileCode, UserService
from django.http import HttpResponse
from zqb_user.forms import SignupEmailForm, SignupMobileForm
import json
from zqb_common.decorators import json_data

# Create your views here.


def user_sign_in(request):
    '''
    User sign in.
    '''
    pass


@json_data
def user_send_mobile_code(request):
    '''
    User send verify code

    mobile: 手机号
    password: 密码
    '''
    signup_form = SignupMobileForm(request.POST)
    if signup_form.is_valid():
        mobile = signup_form.cleaned_data["mobile"]
        # send mobile code
        status, msg = SendMobileCode().send_mobile_code(mobile, request.META.get('HTTP_X_REAL_IP') or request.META['REMOTE_ADDR'])
        if status:
            return {'status': True}
        else:
            return {'status': False, 'error': msg}

    return {'status': False, 'error': signup_form.errors}


@json_data
def user_sign_up_mobile(request):
    '''
    User sign up

    mobile: 手机号
    password: 密码
    '''
    signup_form = SignupMobileForm(request.POST)
    if signup_form.is_valid():
        password = signup_form.cleaned_data["password"]
        mobile = signup_form.cleaned_data["mobile"]
        code = request.POST.get('code', '')

        userservice = UserService()
        if not userservice.verify_mobile_code(mobile=mobile, code=code):
            return {'status': False, 'error': "验证码错误"}
        user = userservice.user_signup(username=mobile, password=password, mobile=mobile)
        if user:
            return {'status': True}
    return {'status': False, 'error': signup_form.errors}


def user_sign_up_email(request):
    '''
    User sign up
    '''
    pass


def upload_user_image(request):
    '''
    Upload user image
    '''
    pass
