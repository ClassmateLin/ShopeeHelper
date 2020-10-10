#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/10 6:26 下午
# @Author  : ClassmateLin
# @Email   : classmatelin@qq.com
# @File    : config.py
# @Desc    : 
import os
import sys

# 根目录
BASE_DIR = os.path.abspath(os.path.splitdrive(sys.argv[0])[0])

# 数据库存放路径
SQLITE_PATH = os.path.join(BASE_DIR, 'sqlite3.db')

# 浏览器驱动
BROWSER_DRIVER = os.path.join(BASE_DIR, 'chrome/chrome.exe')

# 日志目录
LOG_DIR = os.path.join(BASE_DIR, 'logs')

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


MEDIA_DIR = os.path.join(BASE_DIR, 'medias')

AVATAR_IMAGE_PATH = os.path.join(MEDIA_DIR, 'avatar.jpg')

OPTIONS_ICON_DIR = os.path.join(MEDIA_DIR, 'options_icon')

LOADING_GIF_PATH = os.path.join(MEDIA_DIR, 'loading.gif')


PC_INFO_PATH = os.path.join(BASE_DIR, 'sb')

TRAY_ICON = os.path.join(MEDIA_DIR, 'icon128.ico')