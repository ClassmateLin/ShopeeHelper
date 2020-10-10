# -*- coding: utf-8 -*-
# @Time    : 2020/6/17 10:41
# @Author  : ClassmateLin
# @Email   : classmatelin@qq.com
# @File    : stores.py
import json

from peewee import CharField, IntegerField, TextField
from models.base import BaseModel


class StoresModel(BaseModel):
    # 店铺账号
    store_account = CharField(verbose_name='店铺账号', unique=True)

    # 店铺名称
    store_name = CharField(verbose_name='店铺账号', default='')

    # 店铺编码
    store_code = CharField(verbose_name='店铺编号', default='')

    # 粉丝数量
    fans_num = IntegerField(verbose_name='粉丝数量', default=0)

    # 关注数量
    focus_num = IntegerField(verbose_name='关注数量', default=0)

    # cookies
    cookies = TextField(verbose_name='cookies', default='')

    @classmethod
    def import_store(cls, store_account, cookies):
        """
        导入店铺信息
        :param store_account:
        :param cookies:
        :return:
        """
        account = cls.get_or_none(cls.store_account == store_account)
        if not account:
            cls.create(store_account=store_account, cookies=cookies)
        else:
            cls.update(cookies=cookies).where(cls.store_account == store_account)

    @classmethod
    def update_store(cls, store_account, store_name, store_code, focus_num, fans_num):
        """
        更新店铺信息
        :param store_name: 店铺名称
        :param store_account: 店铺账号
        :param store_code: 店铺编码
        :param focus_num: 关注数量
        :param fans_num: 粉丝数量
        :return:
        """
        cls.update(store_code=store_code, store_name=store_name, focus_num=focus_num,
                   fans_num=fans_num).where(cls.store_account == store_account).execute()

    @classmethod
    def delete_store_by_account(cls, store_account):
        """
        通过账号删除店铺
        :param store_account: 账号
        :return:
        """
        cls.delete().where(cls.store_account == store_account).execute()

    @classmethod
    def delete_store_by_id(cls, store_id):
        """
        通过ID删除店铺
        :param store_id:
        :return:
        """
        cls.delete().where(cls.id == store_id).execute()

    @classmethod
    def insert_store(cls, store_account, cookies):
        """
        :param store_account:
        :param cookies:
        :return:
        """
        account = cls.get_or_none(cls.store_account == store_account)
        if not account:
            cls.create(store_account=store_account, cookies=cookies)
        else:
            cls.update(cookies=cookies).where(cls.store_account == store_account).execute()

    @classmethod
    def update_store_cookies(cls, store_account, cookies):
        """
        更新店铺cookies
        :param store_account:
        :param cookies:
        :return:
        """
        cls.update(cookies=cookies).where(cls.store_account == store_account).execute()

    @classmethod
    def get_store_lists(cls):
        results = []
        for obj in cls.select():
            results.append([
                str(obj.id),
                str(obj.store_account),
                str(obj.store_name),
                str(obj.store_code),
                str(obj.fans_num),
                str(obj.focus_num),
                str(obj.cookies)
            ])
        return results

    @classmethod
    def get_store_account_list(cls):
        results = []
        for obj in cls.select():
            results.append(str(obj.store_account))
        return results

    @classmethod
    def get_cookies_by_account(cls, store_account):
        """
        获取cookies
        :param store_account:
        :return:
        """
        cookies = cls.get_or_none(cls.store_account == store_account)
        if not cookies:
            return None
        return json.loads(cookies.cookies)

    @classmethod
    def get_shop_code_by_account(cls, store_account):
        obj = cls.get_or_none(cls.store_account == store_account)
        if not obj:
            return None
        return obj.store_code
