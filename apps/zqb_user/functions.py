# -*- coding: utf-8 -*-

from zqb_common.models import VerifyMobileCode
import logging
import string
from random import choice

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
        pass

    def send_mobile_code(self, mobile, ip, category=1):
        '''
        Send code and save info
        '''

        code = self._generator_code()
        self._send_mobile_code(mobile, code)

        record = VerifyMobileCode()
        record.mobile = mobile
        record.ip = ip
        record.category = category
        record.code = code
        record.save()

        try:
            result = self._send_mobile_code(record.mobile, record.code)
            return result
        except Exception, e:
            logger.error(e)
