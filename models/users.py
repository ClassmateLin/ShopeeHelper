# -*- coding: utf-8 -*-
# @Time    : 2020/6/17 10:47
# @Author  : ClassmateLin
# @Email   : classmatelin@qq.com
# @File    : users.py
from peewee import CharField, TextField

from models.base import BaseModel


class UserModel(BaseModel):
    """
    买家号
    """
    username = CharField(verbose_name='账号')

    password = CharField(verbose_name='密码')

    cookies = TextField(verbose_name='cookies', default='')
