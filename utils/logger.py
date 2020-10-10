#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/10 9:46 下午
# @Author  : ClassmateLin
# @Email   : classmatelin@qq.com
# @File    : logger.py
# @Desc    : 
import os
from conf.config import LOG_DIR

from multiprocessing import Queue
import sys
from loguru import logger


LOG_PATH = os.path.join(LOG_DIR, 'log_{time:YYYY-MM-DD}.log')

logger.add(sys.stderr, format="{time:YYYY-MM-DD} {message}", filter="my_module", level="DEBUG")
logger.add(LOG_PATH, rotation="500 MB", encoding='utf-8')

__q = Queue()


def write_log(msg):
    """
    :return:
    """
    global __q
    logger.debug(str(msg))
    __q.put(str(msg))


def has_log():
    global __q
    return not __q.empty()


def read_log():
    global __q
    return __q.get()
