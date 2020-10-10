#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/12 9:18 下午
# @Author  : ClassmateLin
# @Email   : classmatelin@qq.com
# @File    : files.py
# @Desc    : 
import os


def read_stores_from_dir(dir_path):
    """
    :param dir_path:
    :return:
    """
    res = []
    files = os.listdir(dir_path)
    for filename in files:
        account_name, file_text = os.path.splitext(filename)
        if file_text != '.txt':
            continue
        filepath = os.path.join(dir_path, filename)
        with open(filepath, 'r') as f:
            cookies = f.read()
            res.append({
                'store_account': account_name,
                'cookies': cookies
            })
    return res
