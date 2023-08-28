#!/usr/bin/env python
# coding:utf-8
# @time: 2023/8/22 16:32
# @softaware:PyCharm
# 学习从0-1
import requests
import threading
from datetime import datetime

class DataFetcher_ZDTC:
    def __init__(self):
        self.headers = {
            'Sec-Ch-Ua-Platform': 'Android',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36'
        }

    def fetch_data(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response_json = response.json()

            return response_json
        except Exception as e:
            return {"error": str(e)}


# 时间戳转换

def convert_timestamp_to_date(timestamp) -> object:
    # 将时间戳转换为可读的日期格式,返回几个值：格式 8月22日、2022、20230822、14
    date_str = datetime.fromtimestamp(timestamp).strftime('%#m{m}%#d{d}').format(m='月', d='日')
    date_str_year = datetime.fromtimestamp(timestamp).strftime('%Y')
    date_str_year_d_m = datetime.fromtimestamp(timestamp).strftime('%Y%m%d')
    date_str_year_h = datetime.fromtimestamp(timestamp).strftime('%H')
    limit_up_time = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
    # print(date_str_year_h)        14
    # print(date_str)               8月22日
    # print(date_str_year)          2022
    # print(date_str_year_d_m)      20230822
    # 返回格式 8月22日、2022、20230822、14
    return date_str, date_str_year, date_str_year_d_m, date_str_year_h, limit_up_time





def format_limit_data(data, limit_type, date):

    if limit_type == "涨":
        formatted_output = f"{limit_type}停池：\n当前日期：{data['data']['date']}  {limit_type}停数量：{len(data['data']['info'])}\n"
        formatted_output += f"代码    名称   涨跌幅 当前价 换手率 几天几板 首次涨停时间 最终涨停时间 封板类型 涨停原因\n"
        for entry in data['data']['info']:
            # 首次涨停时间
            first_limit_up_time = convert_timestamp_to_date(int(entry['first_limit_up_time']))[4]
            # 最终涨停时间
            last_limit_up_time = convert_timestamp_to_date(int(entry['last_limit_up_time']))[4]
            formatted_output += f"{entry['code']} {entry['name']} {entry['change_rate']:.2f} {entry['latest']} {entry['turnover_rate']:.2f}% {entry['high_days']} {first_limit_up_time} {last_limit_up_time} {entry['limit_up_type']} {entry['reason_type']}\n"
            # formatted_output += f"{entry['code']} {entry['name']} {entry['change_rate']:.2f} {entry['high_days']} 首次{limit_type}停：{first_limit_up_time} 最终{limit_type}停：{last_limit_up_time} {entry['limit_up_type']} {entry['reason_type']}\n"
    elif limit_type == "跌":
        formatted_output = f"{limit_type}停池：\n当前日期：{data['data']['date']}  {limit_type}停数量：{len(data['data']['info'])}\n"
        formatted_output += f"代码    名称    涨跌幅   当前价 换手率 首次涨停时间 最终涨停时间 \n"
        for entry in data['data']['info']:
            # 首次跌停时间
            first_limit_down_time = convert_timestamp_to_date(int(entry['first_limit_down_time']))[4]
            # 最终跌停时间
            last_limit_down_time = convert_timestamp_to_date(int(entry['last_limit_down_time']))[4]
            formatted_output += f"{entry['code']} {entry['name']} {entry['change_rate']:.2f}% {entry['latest']} {entry['turnover_rate']:.2f}% {first_limit_down_time} {last_limit_down_time}\n"
    elif limit_type == "连":
        formatted_output = f"{limit_type}板池：\n当前日期：{data['data']['date']}  {limit_type}板数量：{len(data['data']['info'])}\n"
        formatted_output += f"代码    名称   涨跌幅 当前价 换手率 几天几板 封板类型 涨停原因\n"
        for entry in data['data']['info']:
            formatted_output += f"{entry['code']} {entry['name']} {entry['change_rate']:.2f} {entry['latest']} {entry['turnover_rate']:.2f}% {entry['high_days']} {entry['limit_up_type']} {entry['reason_type']}\n"
    elif limit_type == "炸":
        formatted_output = f"{limit_type}板池：\n当前日期：{data['data']['date']}  {limit_type}板数量：{len(data['data']['info'])}\n"
        formatted_output += f"代码    名称    涨跌幅  当前价  换手率 \n"
        for entry in data['data']['info']:
            formatted_output += f"{entry['code']} {entry['name']} {entry['change_rate']:.2f}% {entry['latest']} {entry['turnover_rate']:.2f}%\n"
    elif limit_type == "连板天梯":
        formatted_output = f"连板天梯\n当前查询日期：{date}\n"
        for entry in data['data']:
            formatted_output += f"高度：{entry['height']}\n"
            if "code_list" in entry:
                codes = ", ".join([f"{code_entry['code']} {code_entry['name']}" for code_entry in entry["code_list"]])
                formatted_output += codes + "\n"

    return formatted_output


def fetch_limit_data(datename, limit_type):
    url = ""
    date_times = convert_timestamp_to_date(datename)
    date = date_times[2]
    if limit_type == "涨":
        # 填充你的涨停数据请求URL
        url = f"https://data.10jqka.com.cn/dataapi/limit_up/limit_up_pool?page=1&limit=300&field=199112,10,9001,330323,330324,330325,9002,330329,133971,133970,1968584,3475914,900&filter=HS,GEM2STAR&order_field=330329&order_type=0&_=1656565345356&date={date}"
    elif limit_type == "跌":
        # 填充你的跌停数据请求URL
        url = f"https://data.10jqka.com.cn/dataapi/limit_up/lower_limit_pool?page=1&limit=300&field=199112,10,330333,330334,1968584,3475914&filter=HS,GEM2STAR&order_field=199112&order_type=1&_=1656566513120&date={date}"
    elif limit_type == "连":
        # 填充你的跌停数据请求URL
        url = f"https://data.10jqka.com.cn/dataapi/limit_up/continuous_limit_pool?page=1&limit=300&field=199112,10,330329,330325,133971,133970,1968584,3475914,3541450,9001&filter=HS,GEM2STAR&order_field=330329&order_type=0&date={date}"
    elif limit_type == "炸":
        # 填充你的跌停数据请求URL
        url = f"https://data.10jqka.com.cn/dataapi/limit_up/open_limit_pool?page=1&limit=300&field=199112,9002,48,1968584,19,3475914,9003,10&filter=HS,GEM2STAR&order_field=199112&order_type=0&_=1656569328024&date={date}"
    elif limit_type == "连板天梯":
        # 填充你的涨停数据请求URL
        url = f"https://data.10jqka.com.cn/dataapi/limit_up/continuous_limit_up?filter=HS,GEM2STAR&date={date}"


    fetcher = DataFetcher_ZDTC()
    data = fetcher.fetch_data(url)

    if 'error' in data:
        return data['error']
    else:
        formatted_data = format_limit_data(data, limit_type, date)
        return formatted_data





# 定义一个获取数据的函数，并将结果添加到字典中
def fetch_and_store_result(date, limit_type, results_dict):
    result = fetch_limit_data(date, limit_type)
    results_dict[limit_type] = result

# 在主线程中使用多线程
if __name__ == "__main__":
    date = 1692691920  # 设置你的查询日期

    # 创建一个字典用于存储线程结果
    thread_results = {}

    # 创建多个线程来调用不同的数据获取方法
    threads = [
        threading.Thread(target=fetch_and_store_result, args=(date, "涨", thread_results)),
        threading.Thread(target=fetch_and_store_result, args=(date, "跌", thread_results)),
        threading.Thread(target=fetch_and_store_result, args=(date, "连", thread_results)),
        threading.Thread(target=fetch_and_store_result, args=(date, "炸", thread_results)),
        threading.Thread(target=fetch_and_store_result, args=(date, "连板天梯", thread_results))
    ]

    # 启动线程
    for thread in threads:
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    # 打印每个线程的结果
    print(thread_results)
    print("=================================================")
    for limit_type, result in thread_results.items():
        print(f"{result}\n")

    print("所有线程已完成")
