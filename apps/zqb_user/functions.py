# -*- coding: utf-8 -*-

from zqb_common.models import VerifyMobileCode, VerifyEmailUrl
from zqb_common.functions import SaveImage
import logging
import string
from random import choice
from zqb_user.models import UserProfile
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.contrib.auth import authenticate
import datetime
from pytz import utc
from rest_framework.authtoken.models import Token
import requests
import json

logger = logging.getLogger('zqb_user.functions')


def generate_random(random_length, type):
    '''
    随机字符串生成函数
    :param random_length:字符串长度
    :param type:字符串类型（0：纯数字 or 1：数字+字符 or 2：数字+字符+特殊字符）
    :return:生成的随机字符串
    '''
    #随机字符串种子
    if type == 0:
        random_seed = string.digits
    elif type == 1:
        random_seed = string.digits + string.ascii_letters
    elif type == 2:
        random_seed = string.digits + string.ascii_letters + string.punctuation
    random_str = []
    while (len(random_str) < random_length):
        random_str.append(choice(random_seed))
    return ''.join(random_str)


class SendMobileCode():
    '''
    random code send to user
    '''
    def __init__(self):
        pass

    def _generator_code(self, length=6):
        return generate_random(length, 0)

    def _send_mobile_code(self, mobile):
        # TODO:
        data = {
            "mobilePhoneNumber": mobile,
            "ttl" : 30,
            # "name": ""
        }
        headers = {
            'x-lc-id': "nfIkUh9URKD5v7EuA3gkn4KM-gzGzoHsz",
            'x-lc-key': "aLQvOmdY8K2B67fAMDPiz5DU",
            'content-type': "application/json",
        }
        result = requests.request("POST", settings.LEANCLOUD_REQUESTSMSCODE, data=json.dumps(data), headers=headers)
        if result.status_code == 200:
            return ""
        return json.loads(result.text).get('error', "")

    def _verify_mobile_code(self, mobile, code):
        headers = {
            'x-lc-id': "nfIkUh9URKD5v7EuA3gkn4KM-gzGzoHsz",
            'x-lc-key': "aLQvOmdY8K2B67fAMDPiz5DU",
            'content-type': "application/json",
        }
        url = settings.LEANCLOUD_VERIFYSMSCODE + "/%s?mobilePhoneNumber=%s" % (code, mobile)
        result = requests.request("POST", url, headers=headers)
        if result.status_code == 200:
            return ""
        return json.loads(result.text).get('error', "")

    def verify_mobile_code(self, mobile, code, category=0):
        '''
        手机验证码验证
        '''
        try:
            result = self._verify_mobile_code(mobile, code)
            if not result:
                return True
            else:
                return False
        except Exception, e:
            return False
        return True

    def send_mobile_code(self, mobile, ip, category=0):
        '''
        Send code and save info
        '''

        # 验证是否已过时间间隔
        record_list = VerifyMobileCode.objects.filter(Q(mobile=mobile)).order_by("-created")
        if record_list:
            if (datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(minutes=1)) < record_list[0].created:
                return False, '发送太频繁'

        try:
            result = self._send_mobile_code(mobile)
            if result:
                return False, result

            record = VerifyMobileCode()
            record.mobile = mobile
            record.ip = ip
            record.category = category
            record.code = 'leancloud'
            record.save()

            return True, result
        except Exception, e:
            logger.error(e)
            return False


class SendEmailVerify():
    '''
    Send email for verify url
    '''
    def __init__(self):
        pass

    def _generator_code(self, length=10):
        return generate_random(length, 1)

    def _send_email_url(self, email, code):
        # TODO:
        pass

    # TODO:
    def verify_email_url(self, email, code, category=0):
        ''''''
        try:
            record_list = VerifyEmailUrl.objects.filter(Q(email=email), Q(code=code),Q(category=category)).order_by("-created")
            if record_list:
                if (datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(days=1)) > record_list[0].created:
                    return False, '激活链接已经过期'
            else:
                return False
        except Exception, e:
            return False
        return True

    def send_email_url(self, email, ip, category=0):
        '''
        发送邮件验证链接
        '''

        now_time = datetime.datetime.utcnow().replace(tzinfo=utc) - timedelta(hours=23, minutes=59, seconds=59)
        send_count = VerifyEmailUrl.objects.filter(Q(ip=ip), Q(created__gt=now_time)).count()
        if send_count > settings.MAX_SEND_EMAIL_COUNT:
            return False, '每天发送次数超过上限'

        str_code = self._generator_code()

        record = VerifyEmailUrl()
        record.email = email
        record.ip = ip
        record.category = category
        record.code = str_code
        record.save()

        try:
            result = self._send_email_url(record.email, record.code)
            return True, result
        except Exception, e:
            logger.error(e)


class UserService():
    '''
    User service
    '''
    def __init__(self):
        pass

    def upload_user_image(self, user, image_stream, file_type):
        '''
        上传用户图像

        user: 用户对象
        image_stream: 头像流
        '''
        avatar_url = SaveImage(image_stream, file_type=file_type).get_image_url()
        if avatar_url:
            user.avatar_url = avatar_url
            user.save()
            return True
        return False

    def exist_for_user_info(self, info_type, value):
        '''
        判断用户属性是否存在

        info_type: 需要判断字段
        value: 属性值
        '''
        query = {info_type: value}
        user_list = UserProfile.objects.filter(**query)
        if user_list:
            return True
        return False

    def user_signup(self, username, password, email="", mobile=""):
        '''
        Register User
        '''
        user = UserProfile()
        user.username = username
        user.password = make_password(password)
        user.mobile = mobile
        user.email = email
        if email:
            user.is_active = False
        user.avatar_url = settings.DEFAULT_USER_AVATAR_URL

        user.save()
        return user

    def user_signin(self, mobile=None, openid=None, password=None):
        '''
        User login

        mobile: 手机号
        openid: 第三方openid
        password: 密码(mobile 必须有密码)
        '''
        def get_token(user):
            '''get or create user token'''
            usertoken = Token.objects.get_or_create(user=auth_user)
            return True, usertoken[0].key

        # Mobile sign in.
        if mobile and password:
            try:
                user = UserProfile.objects.get(mobile=mobile)
            except UserProfile.DoesNotExist:
                return False, '用户不存在'
            auth_user = authenticate(username=user.username, password=password)
            if auth_user:
                return get_token(auth_user)

        return False, '认证错误'

    def send_signup_email(self, ):
        '''
        发送验证邮箱
        '''

        pass
