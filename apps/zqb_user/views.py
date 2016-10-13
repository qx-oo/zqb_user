# -*- coding: utf-8 -*-

from django.shortcuts import render
import datetime
from zqb_user import functions
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
    '''
    register_form = SignupMobileForm(request.POST)
    if register_form.is_valid():
        mobile = register_form.cleaned_data["mobile"]
        # send mobile code
        functions.SendMobileCode().send_mobile_code(mobile, request.META.get('HTTP_X_REAL_IP') or request.META['REMOTE_ADDR'])

        return {'status': True}

    return {'status': False, 'error': register_form.errors}


def user_sign_up_mobile(request):
    '''
    User sign up
    '''
    register_form = SignupEmailForm(request.POST)
    if register_form.is_valid():
        password = register_form.cleaned_data["password"]
        mobile = register_form.cleaned_data["mobile"]
    pass


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
