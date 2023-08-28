#!/usr/bin/env python
# coding:utf-8
# @time: 2023/8/23 20:35
# @softaware:PyCharm
# 学习从0-1
import time

class Times_tamp_Comparator:
    def __init__(self, input_timestamp ):
        self.input_timestamp = input_timestamp
        self.current_timestamp = int(time.time())
        self.afternoon_0am_timestamp = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d 0:00:00"), "%Y-%m-%d %H:%M:%S")))
        self.afternoon_930am_timestamp = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d 9:30:00"), "%Y-%m-%d %H:%M:%S")))
        self.noon_timestamp = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d 12:00:00"), "%Y-%m-%d %H:%M:%S")))
        self.afternoon_5pm_timestamp = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d 17:00:00"), "%Y-%m-%d %H:%M:%S")))

    def compare(self):
        if self.input_timestamp < self.afternoon_0am_timestamp:
            return 0
        elif self.afternoon_0am_timestamp < self.input_timestamp < self.afternoon_930am_timestamp:
            return 1
        elif self.afternoon_930am_timestamp < self.input_timestamp < self.noon_timestamp:
            return 2
        elif self.noon_timestamp < self.input_timestamp < self.afternoon_5pm_timestamp:
            return 3
        else:
            return 4

# 示例时间戳，表示2023-03-17 00:00:00
# 1692825371  , 2023-08-24 05:16:11
# 1692839771  , 2023-08-24 09:16:11
# 1692738971  , 2023-08-23 05:16:11
# 1692839771  , 2023-08-24 09:16:11
# 1692839771  , 2023-08-24 09:16:11


input_timestamp = 1692738971

comparator = Times_tamp_Comparator(input_timestamp)
result = comparator.compare()
print(result)
