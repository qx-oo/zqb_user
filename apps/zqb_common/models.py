# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone

# Create your models here.


class VerifyMobileCode(models.Model):
    '''
    手机验证码记录
    '''

    mobile = models.CharField(max_length=11, verbose_name="手机号码")
    code = models.CharField(max_length=6, verbose_name="验证码")
    category = models.SmallIntegerField(default=0, choices=((0, "注册"),(1, "忘记密码"),), verbose_name="验证码类型")
    ip = models.CharField(max_length=20, verbose_name="请求来源IP")
    created = models.DateTimeField(default=timezone.now, verbose_name="创建时间")

    class Meta:
        verbose_name = "手机验证记录"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.code


class VerifyEmailUrl(models.Model):
    '''
    邮箱验证记录
    '''

    email = models.CharField(max_length=50, verbose_name="邮箱")
    code = models.CharField(max_length=6, verbose_name="验证码")
    category = models.SmallIntegerField(default=0, choices=((0, "注册"),(1, "忘记密码"),), verbose_name="验证码类型")
    ip = models.CharField(max_length=20, verbose_name="请求来源IP")
    created = models.DateTimeField(default=timezone.now, verbose_name="创建时间")

    class Meta:
        verbose_name = "邮箱验证记录"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.code
