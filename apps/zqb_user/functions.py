# -*- coding: utf-8 -*-

from zqb_common.models import VerifyMobileCode, VerifyEmailUrl
import logging
import string
from random import choice
from zqb_user.models import UserProfile
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.conf import settings
import datetime
from pytz import utc

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

    def _send_mobile_code(self, mobile, code):
        # TODO:
        pass

    def send_mobile_code(self, mobile, ip, category=0):
        '''
        Send code and save info
        '''

        code = self._generator_code()
        self._send_mobile_code(mobile, code)

        # 验证是否已过时间间隔
        record_list = VerifyMobileCode.objects.filter(Q(mobile=mobile)).order_by("-created")
        if record_list:
            if (datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(minutes=1)) < record_list[0].created:
                return False, '发送太频繁'

        record = VerifyMobileCode()
        record.mobile = mobile
        record.ip = ip
        record.category = category
        record.code = code
        record.save()

        try:
            result = self._send_mobile_code(record.mobile, record.code)
            return True, result
        except Exception, e:
            logger.error(e)


class UserService():
    '''
    User service
    '''
    def __init__(self):
        pass

    def user_signup(self, username, password, email="", mobile=""):
        '''
        Register User
        '''
        user = UserProfile()
        user.username = username
        user.password = make_password(password)
        if email:
            user.is_active = False
        user.avatar_url = settings.DEFAULT_USER_AVATAR_URL

        user.save()
        return user

    def verify_mobile_code(self, mobile, code):
        try:
            record_list = VerifyMobileCode.objects.filter(Q(mobile=mobile), Q(code=code),Q(category=0)).order_by("-created")
            if record_list:
                if (datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(minutes=settings.MOBILE_CODE_TIME_OUT)) > record_list[0].created:
                    return False
            else:
                return False
        except Exception, e:
            return False
        return True
