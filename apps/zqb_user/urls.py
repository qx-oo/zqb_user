# -*- coding: utf-8 -*-

from django.conf.urls import url
from rest_framework.authtoken import views
from zqb_user import views


urlpatterns = [
    url(r'^email-signup/', views.user_sign_up_email),
    url(r'^mobile-signup/', views.user_sign_up_mobile),
    url(r'^api-token-auth/', views.obtain_auth_token),
]
