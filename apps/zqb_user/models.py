# -*- coding: utf-8 -*-

# version: 1.0
# author: shawn

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from uuidfield import UUIDField
import datetime


class UserProfileManager(BaseUserManager):

    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        根据用户名和密码创建一个用户
        """
        now = datetime.datetime.now()
        if not email:
            raise ValueError(u'Email必须填写')
        user = self.model(username=username,email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, email, password, True, True,
                                 **extra_fields)


class UserProfile(AbstractBaseUser,PermissionsMixin):
    '''
    Basic user model
    '''
    uuid = UUIDField(auto=True)
    username = models.CharField(verbose_name="用户名", max_length=30, unique=True)
    email = models.EmailField(verbose_name="邮件地址", unique=True, null=True, blank=True)
    mobile = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name=u"手机号码")
    date_joined = models.DateTimeField(verbose_name="创建日期", default=datetime.datetime.now())
    real_name = models.CharField(u'真实姓名', max_length=30, blank=True, null=True)
    # TODO: 暂定七牛云
    # avatar_url = models.ImageField(upload_to="avatar/%Y/%m", default="avatar/default_big.png", max_length=200, blank=True, null=True, verbose_name=u"头像220x220")
    valid_email = models.BooleanField(verbose_name=u"是否验证邮箱", default=False)

    objects = UserProfileManager()

    def send_email_to_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        pass
        # send_mail(subject, message, from_email, [self.email], **kwargs)


class DeviceToken(models.Model):
    '''
    User Device Token
    '''
    device_id = models.CharField("设备ID", max_length=100, unique=True)
    token = models.CharField(max_length=100, unique=True, verbose_name=u"设备Token")
    user = models.ForeignKey(UserProfile, related_name=u"user", verbose_name=u"用户",null=True, blank=True)

    class Meta:
        verbose_name = "DeviceToken"
        verbose_name_plural = verbose_name
        unique_together = (("device_id", "token"),)
        ordering = ['user']