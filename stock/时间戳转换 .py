#!/usr/bin/env python
# coding:utf-8
# @time: 2023/8/22 16:32
# @softaware:PyCharm
# 学习从0-1
import time
from datetime import datetime

class TimestampConverter:
    def __init__(self):
        pass

    def convert_timestamp_to_date(self, timestamp):

        # 将时间戳转换为可读的日期格式,返回几个值：格式 8月22日、2022、20230822、14
        date_str = datetime.fromtimestamp(timestamp).strftime('%#m{m}%#d{d}').format(m='月', d='日')
        date_str_year = datetime.fromtimestamp(timestamp).strftime('%Y')
        date_str_year_d_m = datetime.fromtimestamp(timestamp).strftime('%Y%m%d')
        date_str_year_h = datetime.fromtimestamp(timestamp).strftime('%H')

        # 返回格式 8月22日、2022、20230822、14
        return date_str, date_str_year, date_str_year_d_m, date_str_year_h

if __name__ == '__main__':
    converter = TimestampConverter()
    before = int(time.time())
    x = converter.convert_timestamp_to_date(before)

    print(x[0])
    print(x[1])
    print(x[2])
    print(x[3])



