#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/10 6:28 下午
# @Author  : ClassmateLin
# @Email   : classmatelin@qq.com
# @File    : common.py
# @Desc    : 通用UI
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath, QMovie
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QSharedMemory, pyqtSignal, Qt
from PyQt5.QtNetwork import QLocalSocket, QLocalServer
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QFrame

from conf.config import LOADING_GIF_PATH


__version__ = "0.0.1"


class QSingleApplication(QApplication):
    messageReceived = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(QSingleApplication, self).__init__(*args, **kwargs)
        appid = QApplication.applicationFilePath().lower().split("/")[-1]
        self._socketName = "qtsingleapp-" + appid
        print("socketName", self._socketName)
        self._activationWindow = None
        self._activateOnMessage = False
        self._socketServer = None
        self._socketIn = None
        self._socketOut = None
        self._running = False

        # 先尝试连接
        self._socketOut = QLocalSocket(self)
        self._socketOut.connectToServer(self._socketName)
        self._socketOut.error.connect(self.handleError)
        self._running = self._socketOut.waitForConnected()

        if not self._running:  # 程序未运行
            self._socketOut.close()
            del self._socketOut
            self._socketServer = QLocalServer(self)
            self._socketServer.listen(self._socketName)
            self._socketServer.newConnection.connect(self._onNewConnection)
            self.aboutToQuit.connect(self.removeServer)

    def handleError(self, message):
        print("handleError message: ", message)

    def isRunning(self):
        return self._running

    def activationWindow(self):
        return self._activationWindow

    def setActivationWindow(self, activationWindow, activateOnMessage=True):
        self._activationWindow = activationWindow
        self._activateOnMessage = activateOnMessage

    def activateWindow(self):
        if not self._activationWindow:
            return
        self._activationWindow.setWindowState(
            self._activationWindow.windowState() & ~Qt.WindowMinimized)
        self._activationWindow.raise_()
        self._activationWindow.activateWindow()

    def sendMessage(self, message, msecs=5000):
        if not self._socketOut:
            return False
        if not isinstance(message, bytes):
            message = str(message).encode()
        self._socketOut.write(message)
        if not self._socketOut.waitForBytesWritten(msecs):
            raise RuntimeError("Bytes not written within %ss" %
                               (msecs / 1000.))
        return True

    def _onNewConnection(self):
        if self._socketIn:
            self._socketIn.readyRead.disconnect(self._onReadyRead)
        self._socketIn = self._socketServer.nextPendingConnection()
        if not self._socketIn:
            return
        self._socketIn.readyRead.connect(self._onReadyRead)
        if self._activateOnMessage:
            self.activateWindow()

    def _onReadyRead(self):
        while 1:
            message = self._socketIn.readLine()
            if not message:
                break
            print("Message received: ", message)
            self.messageReceived.emit(message.data().decode())

    def removeServer(self):
        self._socketServer.close()
        self._socketServer.removeServer(self._socketName)


class AvatarLabel(QLabel):

    def __init__(self, image_path='', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setMaximumSize(125, 125)
        self.setMinimumSize(125, 125)
        self.radius = 62.5

        self.target = QPixmap(self.size())  # 大小和控件一样
        self.target.fill(Qt.transparent)  # 填充背景为透明

        p = QPixmap(image_path).scaled(
            # 加载图片并缩放和控件一样大
            125, 125, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        painter = QPainter(self.target)

        # 抗锯齿
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        path = QPainterPath()
        path.addRoundedRect(
            0, 0, self.width(), self.height(), self.radius, self.radius)

        # **** 切割为圆形 ****#
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, p)
        self.setPixmap(self.target)


class BaseFrame(QFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setContentsMargins(0, 0, 0, 0)

        self.gif_frame = QFrame(self)
        self.gif_frame.setMaximumHeight(151)
        self.gif_layout = QHBoxLayout()
        self.gif_layout.setAlignment(Qt.AlignRight)
        self.gif_frame.setLayout(self.gif_layout)
        self.gif_frame.setContentsMargins(0, 0, 0, 0)
        self.gif_layout.setContentsMargins(0, 0, 0, 0)
        # 加载gif图片
        movie = QMovie(LOADING_GIF_PATH)
        label = QLabel(self)
        label.setMaximumSize(151, 109)
        label.setMovie(movie)
        label.setAlignment(Qt.AlignRight)
        label.setContentsMargins(0, 0, 0, 0)
        self.gif_layout.addWidget(label)
        movie.start()
        self.layout().addWidget(self.gif_frame)