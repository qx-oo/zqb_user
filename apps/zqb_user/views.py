# -*- coding: utf-8 -*-

from django.shortcuts import render
import datetime
from zqb_user.functions import SendMobileCode, UserService
from django.http import HttpResponse
from zqb_user.forms import SignupEmailForm, SignupMobileForm
import json
from zqb_common.decorators import json_data
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.parsers import FileUploadParser
import base64

# Create your views here.


@api_view(['POST'])
@permission_classes((AllowAny,))
@json_data
def user_sign_in(request):
    '''
    User sign in.

    mobile: 手机号
    password: 密码
    '''
    if request.POST.get('mobile', None) and request.POST.get('password', None):
        status, token_or_info = UserService().user_signin(mobile=request.POST.get('mobile'),
                                password=request.POST.get('password'))
        if status:
            return {'status': status, 'token': token_or_info}
        else:
            return {'status': status, 'error': token_or_info}
    return {'status': False, 'error': '404'}


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
        status, msg = SendMobileCode().send_mobile_code(mobile, request.META.get('HTTP_X_REAL_IP') or request.META.get('REMOTE_ADDR'))
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
    code: 验证码
    '''
    signup_form = SignupMobileForm(request.POST)
    if signup_form.is_valid():
        password = signup_form.cleaned_data["password"]
        mobile = signup_form.cleaned_data["mobile"]
        code = request.POST.get('code', '')

        if not SendMobileCode().verify_mobile_code(mobile=mobile, code=code):
            return {'status': False, 'error': "验证码错误"}
        user = UserService().user_signup(username=mobile, password=password, mobile=mobile)
        if user:
            return {'status': True}
    return {'status': False, 'error': signup_form.errors}


def user_sign_up_email(request):
    '''
    User sign up
    '''
    pass


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@json_data
def upload_user_image(request):
    '''
    Upload user image

    image_stream: 用户二进制流，需要base64编码
    image_type: 上传图片格式
    '''
    file_stream = request.POST.get("image_stream", None)
    try:
        file_stream = base64.b64decode(file_stream)
    except TypeError:
        return {'status': False, 'error': '类型错误'}
    file_type = request.POST.get("image_type", '.png')
    user = request.user
    if file_stream and user:
        UserService().upload_user_image(user, file_stream, file_type)
    return {'status': False, 'error': '404'}


@api_view(['GET'])
@permission_classes((AllowAny,))
@json_data
def is_exist_user_info(request, info_type, info_value):
    '''
    判断属性是否存在

    info_type: 判断属性
    info_value: 判断属性值
    '''
    info_list = ['mobile', 'username']
    if info_type in info_list:
        status = UserService().exist_for_user_info(info_type, info_value)
        if status:
            return {'status': True, 'is_exist': True}
        else:
            return {'status': True, 'is_exist': False}
    return {'status': False, 'error': '404'}


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@json_data
def get_user_info(self):
    pass


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@json_data
def update_user_info(self):
    pass
