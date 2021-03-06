# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
import re
from zqb_user.models import UserProfile


class SignupEmailForm(forms.Form):
    '''
    邮箱账号注册的Form
    '''
    error_messages = {"duplicate_email": "该账号已被注册",}
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "请输入邮箱账号"}),
                             max_length=30,
                             error_messages = {
                             "required":"账号密码不能为空",
                             "invalid":"注册账号需为邮箱格式",})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "请输入密码"}),
                               min_length=8, max_length=50,
                               error_messages = {
                               "required":"账号密码不能为空",
                               "min_length":"请输入至少8位密码",
                               "max_length":"密码不能超过50位"})

    def clean_email(self):
        '''
        验证Email是否重复
        :return:
        '''
        email = self.cleaned_data["email"]

        # Verify email format
        p = re.compile(settings.REGEX_EMAIL)
        if not p.match(email):
            raise forms.ValidationError(
                self.error_messages['invaild'],
                code='invaild',
                )

        try:
            UserProfile._default_manager.get(email=email)
        except UserProfile.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )



class SignupMobileForm(forms.Form):
    '''
    手机注册表单验证
    '''
    error_messages = {
        "duplicate_mobile": "该账号已被注册",
        "invaild": "注册账号需为手机格式",
        "nonmatch_mobile_code":"手机验证码输入错误，请重试",
        "overdue_mobile_code":"手机验证码已过期，请重试",
    }
    mobile = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-phone fl", "placeholder": "请输入手机号"}),
                             max_length=11, error_messages = {"required":"账号密码不能为空",})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "请输入密码"}),
                               min_length=8, max_length=50,
                               error_messages = {
                                   "required":"账号密码不能为空",
                                   "min_length":"请输入至少8位密码",
                                   "max_length":"密码不能超过50位"})

    def clean_mobile(self):
        '''
        验证Mobile格式是否正确和是否重复
        :return:
        '''
        mobile = self.cleaned_data["mobile"]

        p = re.compile(settings.REGEX_MOBILE)
        if not p.match(mobile):
            raise forms.ValidationError(
                self.error_messages['invaild'],
                code='invaild',
                )

        try:
            UserProfile._default_manager.get(mobile=mobile)
        except UserProfile.DoesNotExist:
            return mobile
        raise forms.ValidationError(
             self.error_messages['duplicate_mobile'],
             code='duplicate_mobile',
        )
