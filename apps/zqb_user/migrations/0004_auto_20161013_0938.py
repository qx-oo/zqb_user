# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-13 09:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zqb_user', '0003_userprofile_is_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'UserInfo', 'verbose_name_plural': 'UserInfo'},
        ),
    ]
