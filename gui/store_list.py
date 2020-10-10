#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/10 6:28 下午
# @Author  : ClassmateLin
# @Email   : classmatelin@qq.com
# @File    : store_list.py
# @Desc    : 店铺列表
import json

from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTableWidget, QAbstractItemView, QPushButton, QMessageBox, \
    QInputDialog, QMenu, QDialog, QHeaderView, QFormLayout, QLabel, QLineEdit, QTextEdit, QTableWidgetItem, \
    QFileDialog, QFrame

from gui.common import BaseFrame, QSingleApplication
from models.stores import StoresModel
from utils.files import read_stores_from_dir


class StoreInsertDialog(QDialog):

    cookies_input = None
    store_input = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self):
        self.resize(350, 100)
        self.setWindowTitle("添加")
        layout = QFormLayout()
        self.setLayout(layout)
        store_label = QLabel('店铺账号:')
        self.store_input = QLineEdit()
        reg = QRegExp("[a-zA-Z0-9_]+$")
        store_validator = QRegExpValidator(self)
        store_validator.setRegExp(reg)
        self.store_input.setValidator(store_validator)
        cookies_label = QLabel('cookies')
        self.cookies_input = QTextEdit()
        layout.addRow(store_label, self.store_input)
        layout.addRow(cookies_label, self.cookies_input)

        button_frame = QFrame()
        button_layout = QHBoxLayout()
        button_frame.setLayout(button_layout)

        accept_button = QPushButton('确认')
        accept_button.clicked.connect(self.accept)

        reject_button = QPushButton('关闭')
        reject_button.clicked.connect(self.reject)

        button_layout.addWidget(accept_button)
        button_layout.addWidget(reject_button)

        layout.addWidget(button_frame)

    def get_data(self):  # 定义获取用户输入数据的方法

        return self.store_input.text(), self.cookies_input.toPlainText()


class StoreListFrame(BaseFrame):
    table_widget = None  # 店铺表格

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self):
        store_widget = QWidget()
        store_widget.setContentsMargins(0, 0, 0, 0)
        store_layout = QHBoxLayout()
        store_layout.setContentsMargins(0, 0, 0, 0)
        store_widget.setLayout(store_layout)
        self.layout().addWidget(store_widget)
        self.table_widget = QTableWidget(store_widget)
        store_layout.addWidget(self.table_widget)
        self.table_widget.setContentsMargins(0, 0, 0, 0)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        titles = ['ID', '店铺账号', '店铺名称', '店铺编号', '粉丝数量', '关注数量', 'cookies']

        QTableWidget.resizeRowsToContents(self.table_widget)  # 设置行高与内容匹配
        QTableWidget.resizeColumnsToContents(self.table_widget)
        self.table_widget.setColumnCount(7)  # 设置表格列数

        self.table_widget.verticalHeader().setVisible(False)  # 设置锤子表格不可见
        self.table_widget.setHorizontalHeaderLabels(titles)  # 设置水平标头

        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self.generate_menu)  # 右键菜单
        self.table_widget.horizontalHeader().setHighlightSections(True)
        self.table_widget.setAlternatingRowColors(True)  # 设置行是否自动变色
        self.table_widget.sortItems(0, Qt.DescendingOrder)  # 指定按第0列排序
        self.reload_table()

        operate_widget = QWidget(self)
        operate_widget.setContentsMargins(0, 10, 0, 0)
        operate_layout = QHBoxLayout()
        insert_button = QPushButton("添加店铺", operate_widget)
        insert_button.setStyleSheet('QPushButton {background-color: #8B8878;min-width: 96px;max-width: '
                                    '96px;min-height: 96px;max-height: 96px;border-radius: 48px; }')
        insert_button.clicked.connect(self.insert_stores)

        import_button = QPushButton("导入店铺", operate_widget)
        import_button.setStyleSheet('QPushButton {background-color: #8B795E;min-width: 96px;max-width: '
                                    '96px;min-height: 96px;max-height: 96px;border-radius: 48px; }')
        import_button.clicked.connect(self.import_stores)

        operate_layout.addWidget(insert_button)
        operate_layout.addWidget(import_button)

        operate_widget.setLayout(operate_layout)
        self.layout().addWidget(operate_widget)

    def insert_stores(self):
        """
        插入店铺
        :return:
        """
        dialog = StoreInsertDialog(self)
        if dialog.exec_():
            store_name, cookies = dialog.get_data()
            if len(store_name) < 1:
                QMessageBox.information(None, '消息', '请输入正确的店铺账号!', QMessageBox.Cancel)
                return
            try:
                json.loads(cookies)
            except Exception as e:
                print(e.args)
                QMessageBox.information(None, '消息', '请输入正确的cookies!', QMessageBox.Cancel)
                return
            StoresModel.insert_store(store_account=store_name, cookies=cookies)
            QMessageBox.information(None, '消息', '添加成功!', QMessageBox.Yes)
            self.reload_table()

    def import_stores(self):
        """
        导入店铺
        :return:
        """
        dir_path = QFileDialog.getExistingDirectory(None, '选择cookies文件夹')
        if dir_path:
            print(dir_path)
            stores_list = read_stores_from_dir(dir_path)
            print(stores_list)
            if len(stores_list) == 0:
                QMessageBox.information(None, '提示', '未找到cookies文件, 请确认文件是否存在!', QMessageBox.Yes)
                return
            total = 0
            string = '共成功导入{}个账号, 如下:\n\t'
            for store in stores_list:
                cookies = store['cookies']
                try:
                    json.loads(cookies)
                except Exception as e:
                    print(e.args)
                    continue
                StoresModel.insert_store(store_account=store['store_account'], cookies=cookies)
                total += 1
                string += store['store_account'] + '\n\t'
            string = string.format(total)
            self.reload_table()
            QMessageBox.information(None, '提示', string, QMessageBox.Yes)

    def reload_table(self):
        """
        :return:
        """
        row_positions = self.table_widget.rowCount()
        for pos in range(0, row_positions)[::-1]:
            self.table_widget.removeRow(pos)

        stores_list = StoresModel.get_store_lists()

        for i in range(len(stores_list)):
            self.table_widget.insertRow(i)
            for j in range(len(stores_list[i])):
                item = QTableWidgetItem(stores_list[i][j])
                item.setTextAlignment(Qt.AlignCenter)
                self.table_widget.setItem(i, j, item)

    def generate_menu(self, pos):
        """
        右键菜单
        :param pos: 行数
        :return:
        """
        menu = QMenu()
        item1 = menu.addAction(u"删除店铺")
        item2 = menu.addAction('更新cookies')
        menu.addAction('复制cookies')

        action = menu.exec_(self.table_widget.mapToGlobal(pos))
        if action == item1:
            store_name = self.table_widget.item(self.table_widget.currentRow(), 1).text()
            store_account = self.table_widget.item(self.table_widget.currentRow(), 1).text()
            is_ok = QMessageBox.information(None, '提示', '是否确认删除店铺: {}?'.format(store_name),
                                            QMessageBox.Yes | QMessageBox.No)
            if is_ok == QMessageBox.Yes:
                self.table_widget.removeRow(self.table_widget.currentRow())
                StoresModel.delete_store_by_account(store_account=store_account)

        elif action == item2:
            cookies, ok = QInputDialog.getMultiLineText(self, "更新cookies", "cookies：",
                                                        '使用google chrome浏览器'
                                                        '\n安装cookie editor插件可导出!')
            if ok:
                try:
                    json.loads(cookies)
                except Exception as e:
                    print(e.args)
                    QMessageBox.information(None, '提示', '输入的cookies非json格式, 无法导入!!!', QMessageBox.Cancel)
                    return
                store_account = self.table_widget.item(self.table_widget.currentRow(), 1).text()
                StoresModel.update_store_cookies(store_account=store_account, cookies=cookies)
                self.table_widget.item(self.table_widget.currentRow(), 6).setText(cookies)

        else:
            clipboard = QSingleApplication.clipboard()
            clipboard.setText(self.table_widget.item(self.table_widget.currentRow(), 6).text())
