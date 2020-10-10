# -*- coding: utf-8 -*-
# @Time    : 2020/6/16 23:49
# @Author  : ClassmateLin
# @Email   : classmatelin@qq.com
# @File    : __init__.py.py
import os
from conf.config import SQLITE_PATH
from .stores import StoresModel
from .users import UserModel


def create_table(*tables):
    u"""
    如果table不存在，新建table
    """
    for table in tables:
        if not table.table_exists():
            table.create_table()


create_table(StoresModel, UserModel)
