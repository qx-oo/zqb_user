# -*- coding: utf-8 -*-

# version: 1.0
# author: shawn

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django_extensions.db.fields import UUIDField
from django.utils import timezone
from django.core.validators import URLValidator
import datetime
from pytz import utc


class UserProfileManager(BaseUserManager):

    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        根据用户名和密码创建一个用户
        """
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        if not email:
            raise ValueError(u'Email必须填写')
        user = self.model(username=username,email=email,
                          is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True,
                                 **extra_fields)


class UserProfile(AbstractBaseUser,PermissionsMixin):
    '''
    Basic user model
    '''
    uuid = UUIDField(auto=True)
    username = models.CharField(verbose_name="用户名", max_length=30, unique=True)
    email = models.EmailField(verbose_name="邮件地址", unique=True, null=True, blank=True)
    mobile = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name=u"手机号码")
    date_joined = models.DateTimeField(verbose_name="创建日期", default=timezone.now)
    real_name = models.CharField(u'真实姓名', max_length=30, blank=True, null=True)
    is_active = models.BooleanField(verbose_name=u"是否活跃", default=True)
    # TODO: 暂定七牛云
    avatar_url = models.TextField(validators=[URLValidator()])
    valid_email = models.BooleanField(verbose_name=u"是否验证邮箱", default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def send_email_to_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        pass
        # send_mail(subject, message, from_email, [self.email], **kwargs)

    class Meta:
        verbose_name = "UserInfo"
        verbose_name_plural = verbose_name


class ThirdpartyOAuth(models.Model):
    '''
    Thirdparty user oauth
    '''
    token = models.CharField(u'令牌', max_length=200)
    partner = models.CharField(u'第三方', max_length=10)
    openid = models.CharField(u'openid', max_length=50)
    user = models.ForeignKey(UserProfile, related_name=u"user", verbose_name=u"用户", null=True, blank=True)
    date_joined = models.DateTimeField(verbose_name="创建日期", default=timezone.now)

    class Meta:
        verbose_name = "第三方用户绑定"
        verbose_name_plural = verbose_name
        unique_together = (('partner', 'openid'),)
        ordering = ['user']
