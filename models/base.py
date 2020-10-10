# -*- coding: utf-8 -*-
# @Time    : 2020/6/17 10:38
# @Author  : ClassmateLin
# @Email   : classmatelin@qq.com
# @File    : base.py
from peewee import Model, SqliteDatabase, BigAutoField

from conf.config import SQLITE_PATH


db = SqliteDatabase(SQLITE_PATH)


class BaseModel(Model):

    id = BigAutoField(primary_key=True)

    class Meta:
        database = db



