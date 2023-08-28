# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import sys
import time, requests

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from datetime import datetime

from chinese_calendar import is_workday

from Ui_A_Ui import Ui_MainWindow
from stock.CX_ths import DataFetcher_ZDTC, fetch_limit_data
from stock.CX_cls import DataFetcher_CLS, fetch_limit_data_cls
from stock.TimeWork import Times_tamp_Comparator


# print(sys.path)

# class MainWindow(QMainWindow, Ui_MainWindow, DataFetcher_ZDTC, DataFetcher_CLS):
class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None, ):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent, )
        self.setupUi(self)
        # 设置主窗口图标
        # self.setWindowIcon(QIcon('123.ico'))
        # 创建一个QTimer定时器
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

    # 当前时间跳动
    def showTime(self):
        # 获取当前时间,设置时间格式
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 在Label上显示时间
        self.label_timelist.setText("当前时间：" + time)

    # 日历点击事件
    def handle_selection_changed(self):
        selected_date = self.calendarWidget.selectedDate()
        current_datetime = QDateTime.currentDateTime()

        if selected_date >= current_datetime.date():
            selected_timestamp = current_datetime.toSecsSinceEpoch()
        else:
            # 设置时间为中午12:00:00
            selected_datetime = QDateTime(selected_date, QTime(17, 0), Qt.TimeSpec.LocalTime)
            # 将所选日期和时间转换为时间戳（秒级）
            selected_timestamp = selected_datetime.toSecsSinceEpoch()

        print("Selected Date:", selected_date.toString(Qt.ISODate))  # Selected Date: 2023-08-18
        print("Selected Timestamp:", selected_timestamp)  # Selected Timestamp: 1692331200
        return selected_timestamp

    # 整理时间信息
    def date_time(self):
        date = datetime.now().date()
        # print(type(date))
        # print(date)
        if is_workday(date):
            print("是工作日")
            return "是工作日"
        else:
            print("是休息日")
            return "是休息日"

    # 加载收盘连板股分析在线图片
    def load_spfx_image(self, url):
        if url == "":
            self.spfx_image.setText("待加载的图片")
        else:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.content
                pixmap = QPixmap()
                pixmap.loadFromData(data)
                self.spfx_image.setPixmap(pixmap.scaledToWidth(300, Qt.SmoothTransformation))
                self.spfx_image.setAlignment(Qt.AlignCenter)
            else:
                self.spfx_image.setText("Failed to load image")

    # 加载午间分析在线图片
    def load_wjfx_image(self, url):
        if url == "":
            self.spfx_image.setText("待加载的图片")
        else:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.content
                pixmap = QPixmap()
                pixmap.loadFromData(data)
                self.wjfx_image.setPixmap(pixmap.scaledToWidth(300, Qt.SmoothTransformation))
                self.wjfx_image.setAlignment(Qt.AlignCenter)
            else:
                self.ztfx_image.setText("Failed to load image")

    # 加载涨停分析在线图片
    def load_ztfx_image(self, url):
        if url == "":
            self.spfx_image.setText("待加载的图片")
        else:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.content
                pixmap = QPixmap()
                pixmap.loadFromData(data)
                self.ztfx_image.setPixmap(pixmap.scaledToWidth(300, Qt.SmoothTransformation))
                self.ztfx_image.setAlignment(Qt.AlignCenter)
            else:
                self.ztfx_image.setText("Failed to load image")

    # 根据返回数字写获取内容并写入
    def number_write(self, number, date):
        if number == 0:
            self.tsxx_text.setText("是工作日，请切换选项卡查看内容")
            print("0====前一天的全部写")
            limit_up_result = fetch_limit_data(date, "涨")
            limit_down_result = fetch_limit_data(date, "跌")
            limit_lb_result = fetch_limit_data(date, "连")
            limit_zb_result = fetch_limit_data(date, "炸")
            limit_lbtt_result = fetch_limit_data(date, "连板天梯")

            # 财联社数据
            limit_wjztfx_result = fetch_limit_data_cls(date, "午间涨停分析")
            limit_ztfx_result = fetch_limit_data_cls(date, "涨停分析")
            limit_lbgfx_result = fetch_limit_data_cls(date, "连板股分析")

            # 写入页面同花顺数据
            self.lbtt_textEdit_lbtt.setText(limit_lbtt_result)
            self.zdtc_textEdit_ztc.setText(limit_up_result)
            self.zdtc_textEdit_dtc.setText(limit_down_result)
            self.lzbc_textEdit_lbc.setText(limit_lb_result)
            self.lzbc_textEdit_zbc.setText(limit_zb_result)

            # 写入页面财联社-午间涨停分析数据
            self.wjfx_bt.setText(limit_wjztfx_result[0])
            self.wjfx_nr.setText(limit_wjztfx_result[1])
            self.wjfx_ming_url.setText(
                f"<a href=\"{limit_wjztfx_result[2]}\" style=\"color:#0000ff;\"><b> {limit_wjztfx_result[2]} </b></a>")
            self.load_wjfx_image(limit_wjztfx_result[2])

            # 写入页面财联社-午间涨停分析数据
            self.ztfx_bt.setText(limit_ztfx_result[0])
            self.ztfx_nr.setText(limit_ztfx_result[1])
            self.ztfx_ming_url.setText(
                f"<a href=\"{limit_ztfx_result[2]}\" style=\"color:#0000ff;\"><b> {limit_ztfx_result[2]} </b></a>")
            self.load_ztfx_image(limit_ztfx_result[2])

            # 写入页面财联社-午间涨停分析数据
            self.spfx_bt.setText(limit_lbgfx_result[0])
            self.spfx_nr.setText(limit_lbgfx_result[1])
            self.spfx_ming_url.setText(
                f"<a href=\"{limit_lbgfx_result[2]}\" style=\"color:#0000ff;\"><b> {limit_lbgfx_result[2]} </b></a>")
            self.load_spfx_image(limit_lbgfx_result[2])

        elif number == 1:
            print("1===9点半之前没有开盘的")
            self.tsxx_text.setText("还没有开盘哦！！！")
            # 同花顺数据
            # limit_up_result = fetch_limit_data(date, "涨")
            # limit_down_result = fetch_limit_data(date, "跌")
            # limit_lb_result = fetch_limit_data(date, "连")
            # limit_zb_result = fetch_limit_data(date, "炸")
            # limit_lbtt_result = fetch_limit_data(date, "连板天梯")

            # 财联社数据
            # limit_wjztfx_result = fetch_limit_data_cls(date, "午间涨停分析")
            # limit_ztfx_result = fetch_limit_data_cls(date, "涨停分析")
            # limit_lbgfx_result = fetch_limit_data_cls(date, "连板股分析")

            # 写入页面同花顺数据
            self.lbtt_textEdit_lbtt.clear()
            self.zdtc_textEdit_ztc.clear()
            self.zdtc_textEdit_dtc.clear()
            self.lzbc_textEdit_lbc.clear()
            self.lzbc_textEdit_zbc.clear()

            # 写入页面财联社-午间涨停分析数据
            self.wjfx_bt.clear()
            self.wjfx_nr.clear()
            self.wjfx_ming_url.clear()
            self.load_wjfx_image("")

            # 写入页面财联社-午间涨停分析数据
            self.ztfx_bt.clear()
            self.ztfx_nr.clear()
            self.ztfx_ming_url.clear()
            self.load_ztfx_image("")

            # 写入页面财联社-午间涨停分析数据
            self.spfx_bt.clear()
            self.spfx_nr.clear()
            self.spfx_ming_url.clear()
            self.load_spfx_image("")

        elif number == 2:
            print("2==9点半-12点的，只写同花顺数据")
            self.tsxx_text.setText("是工作日，请切换选项卡查看内容")
            # 同花顺数据
            limit_up_result = fetch_limit_data(date, "涨")
            limit_down_result = fetch_limit_data(date, "跌")
            limit_lb_result = fetch_limit_data(date, "连")
            limit_zb_result = fetch_limit_data(date, "炸")
            limit_lbtt_result = fetch_limit_data(date, "连板天梯")

            # 财联社数据
            # limit_wjztfx_result = fetch_limit_data_cls(date, "午间涨停分析")
            # limit_ztfx_result = fetch_limit_data_cls(date, "涨停分析")
            # limit_lbgfx_result = fetch_limit_data_cls(date, "连板股分析")

            # 写入页面同花顺数据
            self.lbtt_textEdit_lbtt.setText(limit_lbtt_result)
            self.zdtc_textEdit_ztc.setText(limit_up_result)
            self.zdtc_textEdit_dtc.setText(limit_down_result)
            self.lzbc_textEdit_lbc.setText(limit_lb_result)
            self.lzbc_textEdit_zbc.setText(limit_zb_result)

            # 写入页面财联社-午间涨停分析数据
            self.wjfx_bt.clear()
            self.wjfx_nr.clear()
            self.wjfx_ming_url.clear()
            self.load_wjfx_image("")

            # 写入页面财联社-午间涨停分析数据
            self.ztfx_bt.clear()
            self.ztfx_nr.clear()
            self.ztfx_ming_url.clear()
            self.load_ztfx_image("")

            # 写入页面财联社-午间涨停分析数据
            self.spfx_bt.clear()
            self.spfx_nr.clear()
            self.spfx_ming_url.clear()
            self.load_spfx_image("")

        elif number == 3:
            print("3===12点-17点的，只写同花顺数据和中午收盘数据")
            self.tsxx_text.setText("是工作日，请切换选项卡查看内容")
            # 同花顺数据
            limit_up_result = fetch_limit_data(date, "涨")
            limit_down_result = fetch_limit_data(date, "跌")
            limit_lb_result = fetch_limit_data(date, "连")
            limit_zb_result = fetch_limit_data(date, "炸")
            limit_lbtt_result = fetch_limit_data(date, "连板天梯")

            # 财联社数据
            limit_wjztfx_result = fetch_limit_data_cls(date, "午间涨停分析")
            # limit_ztfx_result = fetch_limit_data_cls(date, "涨停分析")
            # limit_lbgfx_result = fetch_limit_data_cls(date, "连板股分析")

            # 写入页面同花顺数据
            self.lbtt_textEdit_lbtt.setText(limit_lbtt_result)
            self.zdtc_textEdit_ztc.setText(limit_up_result)
            self.zdtc_textEdit_dtc.setText(limit_down_result)
            self.lzbc_textEdit_lbc.setText(limit_lb_result)
            self.lzbc_textEdit_zbc.setText(limit_zb_result)

            # 写入页面财联社-午间涨停分析数据
            self.wjfx_bt.setText(limit_wjztfx_result[0])
            self.wjfx_nr.setText(limit_wjztfx_result[1])
            self.wjfx_ming_url.setText(
                f"<a href=\"{limit_wjztfx_result[2]}\" style=\"color:#0000ff;\"><b> {limit_wjztfx_result[2]} </b></a>")
            self.load_wjfx_image(limit_wjztfx_result[2])

            # 写入页面财联社-午间涨停分析数据
            self.ztfx_bt.clear()
            self.ztfx_nr.clear()
            self.ztfx_ming_url.clear()
            self.load_ztfx_image("")

            # 写入页面财联社-午间涨停分析数据
            self.spfx_bt.clear()
            self.spfx_nr.clear()
            self.spfx_ming_url.clear()
            self.load_spfx_image("")

        elif number == 4:
            print("4===17点以后的全部数据")
            self.tsxx_text.setText("是工作日，请切换选项卡查看内容")
            # 同花顺数据
            limit_up_result = fetch_limit_data(date, "涨")
            limit_down_result = fetch_limit_data(date, "跌")
            limit_lb_result = fetch_limit_data(date, "连")
            limit_zb_result = fetch_limit_data(date, "炸")
            limit_lbtt_result = fetch_limit_data(date, "连板天梯")

            # 财联社数据
            limit_wjztfx_result = fetch_limit_data_cls(date, "午间涨停分析")
            limit_ztfx_result = fetch_limit_data_cls(date, "涨停分析")
            limit_lbgfx_result = fetch_limit_data_cls(date, "连板股分析")

            # 写入页面同花顺数据
            self.lbtt_textEdit_lbtt.setText(limit_lbtt_result)
            self.zdtc_textEdit_ztc.setText(limit_up_result)
            self.zdtc_textEdit_dtc.setText(limit_down_result)
            self.lzbc_textEdit_lbc.setText(limit_lb_result)
            self.lzbc_textEdit_zbc.setText(limit_zb_result)

            # 写入页面财联社-午间涨停分析数据
            self.wjfx_bt.setText(limit_wjztfx_result[0])
            self.wjfx_nr.setText(limit_wjztfx_result[1])
            self.wjfx_ming_url.setText(
                f"<a href=\"{limit_wjztfx_result[2]}\" style=\"color:#0000ff;\"><b> {limit_wjztfx_result[2]} </b></a>")
            self.load_wjfx_image(limit_wjztfx_result[2])

            # 写入页面财联社-午间涨停分析数据
            self.ztfx_bt.setText(limit_ztfx_result[0])
            self.ztfx_nr.setText(limit_ztfx_result[1])
            self.ztfx_ming_url.setText(
                f"<a href=\"{limit_ztfx_result[2]}\" style=\"color:#0000ff;\"><b> {limit_ztfx_result[2]} </b></a>")
            self.load_ztfx_image(limit_ztfx_result[2])

            # 写入页面财联社-午间涨停分析数据
            self.spfx_bt.setText(limit_lbgfx_result[0])
            self.spfx_nr.setText(limit_lbgfx_result[1])
            self.spfx_ming_url.setText(
                f"<a href=\"{limit_lbgfx_result[2]}\" style=\"color:#0000ff;\"><b> {limit_lbgfx_result[2]} </b></a>")
            self.load_spfx_image(limit_lbgfx_result[2])

    # 情况内容，休息日写入内容
    def write_clear(self):
        # 写入提示信息栏
        self.tsxx_text.setText("是休息日或者节假日，请点击日历选择其他日期")
        # 写入页面同花顺数据
        self.lbtt_textEdit_lbtt.clear()
        self.zdtc_textEdit_ztc.clear()
        self.zdtc_textEdit_dtc.clear()
        self.lzbc_textEdit_lbc.clear()
        self.lzbc_textEdit_zbc.clear()

        # 写入页面财联社-午间涨停分析数据
        self.wjfx_bt.clear()
        self.wjfx_nr.clear()
        self.wjfx_ming_url.clear()
        self.wjfx_image.setText("待加载的图片")

        # 写入页面财联社-午间涨停分析数据
        self.ztfx_bt.clear()
        self.ztfx_nr.clear()
        self.ztfx_ming_url.clear()
        self.ztfx_image.setText("待加载的图片")

        # 写入页面财联社-午间涨停分析数据
        self.spfx_bt.clear()
        self.spfx_nr.clear()
        self.spfx_ming_url.clear()
        self.spfx_image.setText("待加载的图片")

    # 按钮点击事件
    @pyqtSlot()
    def on_pushButton_cx_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if_workday = self.date_time()
        if if_workday == "是休息日":
            self.tsxx_text.setText("是休息日或者节假日，请点击日历选择其他日期")
        else:
            date = int(time.time())  # 设置你的查询日期
            # date = 1692691920 # 2023年8月22日 16点
            number_1 = Times_tamp_Comparator(date)
            number = number_1.compare()
            # 执行写入函数
            self.number_write(number, date)

    # 选项卡点击切换事件
    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type int
        """
        # TODO: not implemented yet
        index_name = self.tabWidget.tabText(index)
        text = "是工作日，请切换选项卡查看内容。"
        # 同花顺数据
        self.tsxx_text.setText(f"{text}当前选项卡：{index_name}")
        print(index)
        # raise NotImplementedError

    # 日历点击事件
    @pyqtSlot()
    def on_calendarWidget_selectionChanged(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented ye
        selected_qdate = self.calendarWidget.selectedDate()
        selected_datetime = datetime(selected_qdate.year(), selected_qdate.month(), selected_qdate.day())
        selected_date = selected_datetime.date()
        if not is_workday(selected_date):
            # 是休息日
            self.write_clear()
        else:
            # 是工作日
            date = self.handle_selection_changed()
            print(date)
            number_1 = Times_tamp_Comparator(date)
            number = number_1.compare()
            print(f"==========={number}============")
            # 执行写入函数
            self.number_write(number, date)


'''
    if number == 0:
            print("0")
            limit_up_result = fetch_limit_data(date, "涨")
            limit_down_result = fetch_limit_data(date, "跌")
            limit_lb_result = fetch_limit_data(date, "连")
            limit_zb_result = fetch_limit_data(date, "炸")
            limit_lbtt_result = fetch_limit_data(date, "连板天梯")

            # 财联社数据
            limit_wjztfx_result = fetch_limit_data_cls(date, "午间涨停分析")
            limit_ztfx_result = fetch_limit_data_cls(date, "涨停分析")
            limit_lbgfx_result = fetch_limit_data_cls(date, "连板股分析")

            # 写入页面同花顺数据
            self.lbtt_textEdit_lbtt.setText(limit_lbtt_result)
            self.zdtc_textEdit_ztc.setText(limit_up_result)
            self.zdtc_textEdit_dtc.setText(limit_down_result)
            self.lzbc_textEdit_lbc.setText(limit_lb_result)
            self.lzbc_textEdit_zbc.setText(limit_zb_result)

            # 写入页面财联社-午间涨停分析数据
            self.wjfx_bt.setText(limit_wjztfx_result[0])
            self.wjfx_nr.setText(limit_wjztfx_result[1])
            self.wjfx_ming_url.setText(
                f"<a href=\"{limit_wjztfx_result[2]}\" style=\"color:#0000ff;\"><b> {limit_wjztfx_result[2]} </b></a>")

            # 写入页面财联社-午间涨停分析数据
            self.ztfx_bt.setText(limit_ztfx_result[0])
            self.ztfx_nr.setText(limit_ztfx_result[1])
            self.ztfx_ming_url.setText(
                f"<a href=\"{limit_ztfx_result[2]}\" style=\"color:#0000ff;\"><b> {limit_ztfx_result[2]} </b></a>")

            # 写入页面财联社-午间涨停分析数据
            self.spfx_bt.setText(limit_lbgfx_result[0])
            self.spfx_nr.setText(limit_lbgfx_result[1])
            self.spfx_ming_url.setText(
                f"<a href=\"{limit_lbgfx_result[2]}\" style=\"color:#0000ff;\"><b> {limit_lbgfx_result[2]} </b></a>")
        elif number == 1:
            print("1")
            self.tsxx_text.setText("还没有开盘哦！！！")
            # 同花顺数据
            # limit_up_result = fetch_limit_data(date, "涨")
            # limit_down_result = fetch_limit_data(date, "跌")
            # limit_lb_result = fetch_limit_data(date, "连")
            # limit_zb_result = fetch_limit_data(date, "炸")
            # limit_lbtt_result = fetch_limit_data(date, "连板天梯")

            # 财联社数据
            # limit_wjztfx_result = fetch_limit_data_cls(date, "午间涨停分析")
            # limit_ztfx_result = fetch_limit_data_cls(date, "涨停分析")
            # limit_lbgfx_result = fetch_limit_data_cls(date, "连板股分析")

            # 写入页面同花顺数据
            self.lbtt_textEdit_lbtt.clear()
            self.zdtc_textEdit_ztc.clear()
            self.zdtc_textEdit_dtc.clear()
            self.lzbc_textEdit_lbc.clear()
            self.lzbc_textEdit_zbc.clear()

            # 写入页面财联社-午间涨停分析数据
            self.wjfx_bt.clear()
            self.wjfx_nr.clear()
            self.wjfx_ming_url.clear()

            # 写入页面财联社-午间涨停分析数据
            self.ztfx_bt.clear()
            self.ztfx_nr.clear()
            self.ztfx_ming_url.clear()

            # 写入页面财联社-午间涨停分析数据
            self.spfx_bt.clear()
            self.spfx_nr.clear()
            self.spfx_ming_url.clear()

        elif number == 2:
            print("2")
            # self.tsxx_text.setText("！！！")
            limit_up_result = fetch_limit_data(date, "涨")
            limit_down_result = fetch_limit_data(date, "跌")
            limit_lb_result = fetch_limit_data(date, "连")
            limit_zb_result = fetch_limit_data(date, "炸")
            limit_lbtt_result = fetch_limit_data(date, "连板天梯")

            # 财联社数据
            # limit_wjztfx_result = fetch_limit_data_cls(date, "午间涨停分析")
            # limit_ztfx_result = fetch_limit_data_cls(date, "涨停分析")
            # limit_lbgfx_result = fetch_limit_data_cls(date, "连板股分析")

            # 写入页面同花顺数据
            self.lbtt_textEdit_lbtt.setText(limit_lbtt_result)
            self.zdtc_textEdit_ztc.setText(limit_up_result)
            self.zdtc_textEdit_dtc.setText(limit_down_result)
            self.lzbc_textEdit_lbc.setText(limit_lb_result)
            self.lzbc_textEdit_zbc.setText(limit_zb_result)

            # 写入页面财联社-午间涨停分析数据
            self.wjfx_bt.clear()
            self.wjfx_nr.clear()
            self.wjfx_ming_url.clear()

            # 写入页面财联社-午间涨停分析数据
            self.ztfx_bt.clear()
            self.ztfx_nr.clear()
            self.ztfx_ming_url.clear()

            # 写入页面财联社-午间涨停分析数据
            self.spfx_bt.clear()
            self.spfx_nr.clear()
            self.spfx_ming_url.clear()

        elif number == 3:
            print("3")
            limit_up_result = fetch_limit_data(date, "涨")
            limit_down_result = fetch_limit_data(date, "跌")
            limit_lb_result = fetch_limit_data(date, "连")
            limit_zb_result = fetch_limit_data(date, "炸")
            limit_lbtt_result = fetch_limit_data(date, "连板天梯")

            # 财联社数据
            limit_wjztfx_result = fetch_limit_data_cls(date, "午间涨停分析")
            # limit_ztfx_result = fetch_limit_data_cls(date, "涨停分析")
            # limit_lbgfx_result = fetch_limit_data_cls(date, "连板股分析")

            # 写入页面同花顺数据
            self.lbtt_textEdit_lbtt.setText(limit_lbtt_result)
            self.zdtc_textEdit_ztc.setText(limit_up_result)
            self.zdtc_textEdit_dtc.setText(limit_down_result)
            self.lzbc_textEdit_lbc.setText(limit_lb_result)
            self.lzbc_textEdit_zbc.setText(limit_zb_result)

            # 写入页面财联社-午间涨停分析数据
            self.wjfx_bt.setText(limit_wjztfx_result[0])
            self.wjfx_nr.setText(limit_wjztfx_result[1])
            self.wjfx_ming_url.setText(
                f"<a href=\"{limit_wjztfx_result[2]}\" style=\"color:#0000ff;\"><b> {limit_wjztfx_result[2]} </b></a>")

            # 写入页面财联社-午间涨停分析数据
            self.ztfx_bt.clear()
            self.ztfx_nr.clear()
            self.ztfx_ming_url.clear()

            # 写入页面财联社-午间涨停分析数据
            self.spfx_bt.clear()
            self.spfx_nr.clear()
            self.spfx_ming_url.clear()

        elif number == 4:
            print("4")
            limit_up_result = fetch_limit_data(date, "涨")
            limit_down_result = fetch_limit_data(date, "跌")
            limit_lb_result = fetch_limit_data(date, "连")
            limit_zb_result = fetch_limit_data(date, "炸")
            limit_lbtt_result = fetch_limit_data(date, "连板天梯")

            # 财联社数据
            limit_wjztfx_result = fetch_limit_data_cls(date, "午间涨停分析")
            limit_ztfx_result = fetch_limit_data_cls(date, "涨停分析")
            limit_lbgfx_result = fetch_limit_data_cls(date, "连板股分析")

            # 写入页面同花顺数据
            self.lbtt_textEdit_lbtt.setText(limit_lbtt_result)
            self.zdtc_textEdit_ztc.setText(limit_up_result)
            self.zdtc_textEdit_dtc.setText(limit_down_result)
            self.lzbc_textEdit_lbc.setText(limit_lb_result)
            self.lzbc_textEdit_zbc.setText(limit_zb_result)

            # 写入页面财联社-午间涨停分析数据
            self.wjfx_bt.setText(limit_wjztfx_result[0])
            self.wjfx_nr.setText(limit_wjztfx_result[1])
            self.wjfx_ming_url.setText(
                f"<a href=\"{limit_wjztfx_result[2]}\" style=\"color:#0000ff;\"><b> {limit_wjztfx_result[2]} </b></a>")

            # 写入页面财联社-午间涨停分析数据
            self.ztfx_bt.setText(limit_ztfx_result[0])
            self.ztfx_nr.setText(limit_ztfx_result[1])
            self.ztfx_ming_url.setText(
                f"<a href=\"{limit_ztfx_result[2]}\" style=\"color:#0000ff;\"><b> {limit_ztfx_result[2]} </b></a>")

            # 写入页面财联社-午间涨停分析数据
            self.spfx_bt.setText(limit_lbgfx_result[0])
            self.spfx_nr.setText(limit_lbgfx_result[1])
            self.spfx_ming_url.setText(
                f"<a href=\"{limit_lbgfx_result[2]}\" style=\"color:#0000ff;\"><b> {limit_lbgfx_result[2]} </b></a>")

        # # 同花顺数据
        # limit_up_result = fetch_limit_data(date, "涨")
        # limit_down_result = fetch_limit_data(date, "跌")
        # limit_lb_result = fetch_limit_data(date, "连")
        # limit_zb_result = fetch_limit_data(date, "炸")
        # limit_lbtt_result = fetch_limit_data(date, "连板天梯")
        #
        # # 财联社数据
        # limit_wjztfx_result = fetch_limit_data_cls(date, "午间涨停分析")
        # limit_ztfx_result = fetch_limit_data_cls(date, "涨停分析")
        # limit_lbgfx_result = fetch_limit_data_cls(date, "连板股分析")
        #
        #
        # # 写入页面同花顺数据
        # self.lbtt_textEdit_lbtt.setText(limit_lbtt_result)
        # self.zdtc_textEdit_ztc.setText(limit_up_result)
        # self.zdtc_textEdit_dtc.setText(limit_down_result)
        # self.lzbc_textEdit_lbc.setText(limit_lb_result)
        # self.lzbc_textEdit_zbc.setText(limit_zb_result)
        #
        # # 写入页面财联社-午间涨停分析数据
        # self.wjfx_bt.setText(limit_wjztfx_result[0])
        # self.wjfx_nr.setText(limit_wjztfx_result[1])
        # self.wjfx_ming_url.setText(f"<a href=\"{limit_wjztfx_result[2]}\" style=\"color:#0000ff;\"><b> {limit_wjztfx_result[2]} </b></a>")
        #
        # # 写入页面财联社-午间涨停分析数据
        # self.ztfx_bt.setText(limit_ztfx_result[0])
        # self.ztfx_nr.setText(limit_ztfx_result[1])
        # self.ztfx_ming_url.setText(f"<a href=\"{limit_ztfx_result[2]}\" style=\"color:#0000ff;\"><b> {limit_ztfx_result[2]} </b></a>")
        #
        # # 写入页面财联社-午间涨停分析数据
        # self.spfx_bt.setText(limit_lbgfx_result[0])
        # self.spfx_nr.setText(limit_lbgfx_result[1])
        # self.spfx_ming_url.setText(f"<a href=\"{limit_lbgfx_result[2]}\" style=\"color:#0000ff;\"><b> {limit_lbgfx_result[2]} </b></a>")


        # raise NotImplementedError
'''

if __name__ == "__main__":
    import sys

    App = QApplication(sys.argv)
    Ui = MainWindow()
    Ui.show()
    sys.exit(App.exec())
