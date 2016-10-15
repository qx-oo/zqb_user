# -*- coding: utf-8 -*-

from django.conf.urls import url
from rest_framework.authtoken import views as authtoken_views
from zqb_user import views


urlpatterns = [
    url(r'^mobile-signup/$', views.user_sign_up_mobile), # 手机用户注册
    url(r'^mobile-sendcode/$', views.user_send_mobile_code), # 发送手机验证码
    url(r'^signin/$', views.user_sign_in), # 用户登陆
    url(r'^upload-avatar/$', views.upload_user_image), # 上传用户头像
    url(r'^exists/(?P<info_type>[^/]+)/(?P<info_value>[^/]+)/$', views.is_exist_user_info), # 上传用户头像
    # url(r'^api-token-auth/', authtoken_views.obtain_auth_token),
    # url(r'^test/', views.test),
]
