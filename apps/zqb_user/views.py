# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.

def user_sign_in(request):
    '''
    User sign in.
    '''
    pass


def user_sign_up_mobile(request):
    '''
    User sign up
    '''
    register_form = SignupEmailForm(request.POST)
    if register_form.is_valid():
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
