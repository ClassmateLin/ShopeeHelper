#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/10 6:22 下午
# @Author  : ClassmateLin
# @Email   : classmatelin@qq.com
# @File    : main.py
# @Desc    : 主程序
import sys
import time
import os
import threading
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget, QFrame, QSizePolicy,
    QVBoxLayout, QHBoxLayout, QStackedWidget,
    QSystemTrayIcon, QTextBrowser,
    QLabel, QListWidget, QListWidgetItem,
    QMenu, QAction, QStyle, qApp)

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon, QMovie


from conf.config import AVATAR_IMAGE_PATH, OPTIONS_ICON_DIR, LOADING_GIF_PATH, TRAY_ICON
from utils.logger import read_log, has_log
from gui.store_list import StoreListFrame
from gui.live_fans import LiveFansFrame
from gui.goods_like import GoodsLikeFrame
from gui.store_pv import StorePVFrame
from gui.common import AvatarLabel, QSingleApplication


OPTIONS = [
    '店铺列表',
    '店铺死粉',
    '商品点赞',
    '商品浏览',
]

FRAMES = [
    StoreListFrame,
    LiveFansFrame,
    GoodsLikeFrame,
    GoodsLikeFrame,
    StorePVFrame
]


class MainWindow(QMainWindow):
    """
    主窗体
    """
    tray_icon = None  # 托盘图标
    base_widget = None  # 界面最基础容器
    base_layout = None  # 界面最基础布局
    left_frame = None  # 界面左边容器
    left_layout = None  # 界面左边布局
    right_frame = None  # 界面右边容器
    right_layout = None  # 界面右边布局
    option_frame = None  # 功能选项容器
    option_list_widget = None  # 左侧功能选项
    option_stack_widget = None  # 右侧功能页面
    log_widget = None  # 右侧日志界面
    log_text = None  # 日志框
    log_text_signal = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.init_window()
        self.init_tray()
        self.log_text_signal.connect(self.append_text)
        threading.Thread(target=self.read_log).start()

    def init_window(self):
        """
        初始化窗体
        :return:
        """
        self.setWindowTitle("虾皮助手")
        self.setMinimumSize(QSize(800, 600))
        self.setStyleSheet("background-color: rgb(248,248, 255)")

        # 基础容器定义
        self.base_widget = QWidget(self)
        self.base_layout = QHBoxLayout()
        self.base_widget.setLayout(self.base_layout)
        self.setCentralWidget(self.base_widget)

        # 左边容器定义
        self.left_frame = QFrame(self.base_widget)
        self.init_left_frame()

        # 右边容器定义
        self.right_frame = QFrame(self.base_widget)
        self.init_right_frame()
        self.base_layout.addWidget(self.left_frame)
        self.base_layout.addWidget(self.right_frame)

    def init_left_frame(self):
        """
        初始化左边容器
        :return:
        """
        self.left_layout = QVBoxLayout()
        self.left_frame.setLayout(self.left_layout)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_frame.setContentsMargins(0, 20, 0, 0)
        self.left_frame.setMinimumWidth(125)
        self.left_frame.setMaximumWidth(125)
        self.left_frame.setStyleSheet("background-color: rgb(222,248, 255)")
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(1)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.left_frame.sizePolicy().hasHeightForWidth())
        self.left_frame.setSizePolicy(size_policy)

        avatar_label = AvatarLabel(image_path=AVATAR_IMAGE_PATH)
        self.left_layout.addWidget(avatar_label)

        self.option_frame = QWidget()
        self.option_frame.setContentsMargins(0, 30, 0, 0)
        option_layout = QVBoxLayout()
        option_layout.setContentsMargins(0, 0, 0, 0)
        self.option_frame.setLayout(option_layout)
        self.option_list_widget = QListWidget()
        self.option_list_widget.setContentsMargins(0, 0, 0, 0)
        option_layout.addWidget(self.option_list_widget)

        for i in range(len(OPTIONS)):
            item = QListWidgetItem()
            item.setText(OPTIONS[i])
            item.setIcon(QIcon(os.path.join(OPTIONS_ICON_DIR, '{}.png'.format(i + 1))))
            item.setTextAlignment(Qt.AlignCenter)
            item.setSizeHint(QSize(125, 25))
            self.option_list_widget.addItem(item)

        self.option_list_widget.setFrameStyle(QListWidget.NoFrame)
        self.left_layout.addWidget(self.option_frame)

    def init_right_frame(self):
        """
        初始化右边容器
        :return:
        """
        self.right_layout = QVBoxLayout()
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_frame.setContentsMargins(0, 0, 0, 0)
        self.right_frame.setLayout(self.right_layout)
        self.right_frame.setStyleSheet("background-color: rgb(248,248, 255)")
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(4)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.right_frame.sizePolicy().hasHeightForWidth())
        self.right_frame.setSizePolicy(size_policy)

        self.option_stack_widget = QStackedWidget()
        self.option_list_widget.setMinimumHeight(600)
        self.option_stack_widget.setContentsMargins(0, 0, 0, 0)
        self.option_list_widget.currentRowChanged.connect(
            self.option_stack_widget.setCurrentIndex)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(10)
        size_policy.setHeightForWidth(self.option_stack_widget.sizePolicy().hasHeightForWidth())

        for frame in FRAMES:
            obj = frame()
            self.option_stack_widget.addWidget(obj)

        self.log_widget = QWidget()
        self.log_widget.setMaximumHeight(200)
        self.log_widget.setContentsMargins(0, 0, 0, 0)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(1)
        size_policy.setHeightForWidth(self.log_widget.sizePolicy().hasHeightForWidth())
        log_layout = QVBoxLayout()
        log_layout.setContentsMargins(0, 0, 0, 0)
        self.log_widget.setLayout(log_layout)
        log_label = QLabel('日志记录')
        log_label.setContentsMargins(0, 0, 0, 0)
        log_label.setAlignment(Qt.AlignCenter)
        self.log_text = QTextBrowser()
        self.log_text.setContentsMargins(0, 0, 0, 0)
        self.log_text.setAlignment(Qt.AlignLeft)

        log_layout.addWidget(log_label)
        log_layout.addWidget(self.log_text)

        self.right_layout.addWidget(self.option_stack_widget)
        self.right_layout.addWidget(self.log_widget)

    @pyqtSlot(str)
    def append_text(self, text):
        self.log_text.append(text)

    def read_log(self):
        while True:
            while has_log():
                msg = read_log()
                self.log_text_signal.emit(msg)
                time.sleep(0.05)
            time.sleep(0.1)

    def exit(self):
        self.tray_icon = None
        os._exit(0)

    def init_tray(self):
        """
        初始化系统托盘
        :return:
        """
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(TRAY_ICON))
        show_action = QAction("显示窗口", self)
        quit_action = QAction("退出程序", self)
        hide_action = QAction("隐藏窗口", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(self.exit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def closeEvent(self, event):
        """
        重写右上角X操作的事件
        :param event:
        :return:
        """
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "虾皮助手",
            "应用已收起至托盘!!!",
            QSystemTrayIcon.Information,
            2000
        )


if __name__ == '__main__':
    app = QSingleApplication(sys.argv)
    window = MainWindow()
    app.setActivationWindow(window)
    app.messageReceived.connect(window.append_text)
    window.show()
    sys.exit(app.exec_())
