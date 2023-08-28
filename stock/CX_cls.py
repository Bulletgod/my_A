#!/usr/bin/env python
# coding:utf-8
# @time: 2023/8/22 16:32
# @softaware:PyCharm
# 学习从0-1
import re
from datetime import datetime
import requests

class DataFetcher_CLS:
    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'Cookie': 'HWWAFSESID=c817b1d211748890cec; HWWAFSESTIME=1668563388113; hasTelegraphNotification=on; hasTelegraphRemind=on; hasTelegraphSound=on; vipNotificationState=on; isMinimize=off; wafatcltime=1668563430580; wafatclconfirm=lVgU1DlApVzf2W8mhpSJE+PQDSvOaHb+4moCqmK5hX/MHH90QLUIJWB0ne3E0kjTVL+BUe7DMPZV72a9XR8HldYgGey9NLgjIaUjxp4zWhIqI2onYR/TFobsWrvAXxQnBRE2YxkEtLClXK7ZaHXxQmlLj7hPzrcbhuPXei0AjmemBn0dfacrwnAcMrfgqdZy5Z5lKbzE3AKEJEUz9JhL7jPPnIubgigNhj45HeKF5OH7baeOcZtnwLZk68T+oZnIbgfC6x6sD2ioxX6TXzKM9Yhxv0dNM1PfF7WW6K7Nc1UA+wjUbgWByndxfEe2OLJs+sYKVcMkvXoAUhT0PudYlkFm5pUoYMjH3A0m3BmQ/dI94BE4EhwtkeoMQxK0KG0SXWFTLXHaEgVyXBQFfIYgKsFnTqwwmcVLxE+auj2MSDfAzWSe3PD+wE/ORd2tKeBhlabfzbyp6+3Q5A59h3KNrkWp4zYAXiyN0T7/Nh5A9rG6+clNWT+dP+aC8dMt4WNlic8NXGN0hcFZPamkUBBsNdr9vpUmrAbodiG2gmG+khKDTaUkSsjNHiLgBZYMTXY6bKSG16Wl1LUWYeUjVf8p9wqM0PW7QdFYd4abOcs9MkqwaV3ZACfJLKqFhlFbw/5Te+D58oDM1wUYGGkwui8PwIMsMXD/fvKuN0xcx4A5Rz3Ed8WmE7LVoBb7hoRiynq6ke8YiWv/aSPtGyMcik8/EYjBLMk1TonUPrDAecN55RdH7mMf3gGRFeDuYfVJcAfQw0uymm3eF7vL2Oy8DRe7rQ%3D%3D; wafatcltoken=fce61e64046593162e9722228ad32a78Cookie: HWWAFSESID=c817b1d211748890cec; HWWAFSESTIME=1668563388113; hasTelegraphNotification=on; hasTelegraphRemind=on; hasTelegraphSound=on; vipNotificationState=on; isMinimize=off; wafatcltime=1668563430580; wafatclconfirm=lVgU1DlApVzf2W8mhpSJE+PQDSvOaHb+4moCqmK5hX/MHH90QLUIJWB0ne3E0kjTVL+BUe7DMPZV72a9XR8HldYgGey9NLgjIaUjxp4zWhIqI2onYR/TFobsWrvAXxQnBRE2YxkEtLClXK7ZaHXxQmlLj7hPzrcbhuPXei0AjmemBn0dfacrwnAcMrfgqdZy5Z5lKbzE3AKEJEUz9JhL7jPPnIubgigNhj45HeKF5OH7baeOcZtnwLZk68T+oZnIbgfC6x6sD2ioxX6TXzKM9Yhxv0dNM1PfF7WW6K7Nc1UA+wjUbgWByndxfEe2OLJs+sYKVcMkvXoAUhT0PudYlkFm5pUoYMjH3A0m3BmQ/dI94BE4EhwtkeoMQxK0KG0SXWFTLXHaEgVyXBQFfIYgKsFnTqwwmcVLxE+auj2MSDfAzWSe3PD+wE/ORd2tKeBhlabfzbyp6+3Q5A59h3KNrkWp4zYAXiyN0T7/Nh5A9rG6+clNWT+dP+aC8dMt4WNlic8NXGN0hcFZPamkUBBsNdr9vpUmrAbodiG2gmG+khKDTaUkSsjNHiLgBZYMTXY6bKSG16Wl1LUWYeUjVf8p9wqM0PW7QdFYd4abOcs9MkqwaV3ZACfJLKqFhlFbw/5Te+D58oDM1wUYGGkwui8PwIMsMXD/fvKuN0xcx4A5Rz3Ed8WmE7LVoBb7hoRiynq6ke8YiWv/aSPtGyMcik8/EYjBLMk1TonUPrDAecN55RdH7mMf3gGRFeDuYfVJcAfQw0uymm3eF7vL2Oy8DRe7rQ%3D%3D; wafatcltoken=fce61e64046593162e9722228ad32a78'
        }


    # 一次请求获取ID
    def fetch_data(self, url):
        try:
            payload = {}
            response = requests.request("GET", url, headers=self.headers, data=payload)
            response_json = response.json()
            return response_json
        except Exception as e:
            return {"error": str(e)}

    # 二次请求获取内容和图片地址
    def get_url1(self, id):
        url = f"https://api3.cls.cn/share/article/{id}?s=android&sv=7.8.9&app=cailianpress"
        payload = {}
        response = requests.request("GET", url, headers=self.headers, data=payload)
        html = response.text
        # return html

        # # 正则
        # def extract_patterns_from_html(html):
        # 正则表达式
        pattern1 = r'<title>(.*?)</titl'
        pattern2 = r'telegraph-content content\">([\s\S]*?)</div>'
        pattern3 = r'data-src=\"(.*?)\" />'
        # 正则表达式列表
        patterns = [pattern1, pattern2, pattern3]
        # results = {}
        results = []

        for pattern in patterns:
            compiled_pattern = re.compile(pattern, re.DOTALL)
            match = compiled_pattern.search(html)

            if match:
                extracted_text = match.group(1)
                extracted_text = extracted_text.strip()
                cleaned_text = ' '.join(extracted_text.split())
                results.append(cleaned_text)
                # return results[pattern]
            else:
                results = "没有找到相关数据。"

        return results


# 时间戳转换

def convert_timestamp_to_date(timestamp):
    # 将时间戳转换为可读的日期格式,返回几个值：格式 8月22日、2022、20230822、14
    date_str = datetime.fromtimestamp(timestamp).strftime('%#m{m}%#d{d}').format(m='月', d='日')
    date_str_year = datetime.fromtimestamp(timestamp).strftime('%Y')
    date_str_year_d_m = datetime.fromtimestamp(timestamp).strftime('%Y%m%d')
    date_str_year_h = datetime.fromtimestamp(timestamp).strftime('%H')
    # print(date_str_year_h)        14
    # print(date_str)               8月22日
    # print(date_str_year)          2022
    # print(date_str_year_d_m)      20230822
    # 返回格式 8月22日、2022、20230822、14
    return date_str, date_str_year,date_str_year_d_m,date_str_year_h



def format_limit_data(data, limit_type, date_times):

    matching_ids = []
    datename_year = date_times

    if limit_type == "午间涨停分析":
        for entry in data['data']['telegram']['data']:
            id_time = [id_id, time] = [f"{entry['id']}", f"{entry['time']}"]
            matching_ids.append(id_time)

        for list_time in matching_ids:
            list_time_year = convert_timestamp_to_date(int(list_time[1]))
            if list_time_year[1] == datename_year[1]:
                id_id = list_time[0]
                return id_id
            else:
                id_id = "id错误"
                return id_id

    elif limit_type == "涨停分析":
        # matching_ids = []
        for entry in data['data']['telegram']['data']:
            id_time = [id_id, time] = [f"{entry['id']}", f"{entry['time']}"]
            matching_ids.append(id_time)
            # print(id,time)
        print(matching_ids)
        # print(matching_ids[0])
        # print(matching_ids[0][1])
        for list_time in matching_ids:
            # print(list_time)
            # print(list_time[1])
            list_time_year = convert_timestamp_to_date(int(list_time[1]))
            # print(type(list_time_year))
            if list_time_year[1] == datename_year[1]:
                id_id = list_time[0]
                # print(f"id:======{id_id}=============time======{list_time_year}========={list_time_year[0]}========={ list_time[1]}========")
                return id_id
            else:
                id_id = "id错误"
                # print(f"id:======{id_id}=============time======{list_time_year}========={list_time_year[0]}========={ list_time[1]}========")
                return id_id

    elif limit_type == "连板股分析":
        for entry in data['data']['telegram']['data']:
            id_time = [id_id, time] = [f"{entry['id']}", f"{entry['time']}"]
            matching_ids.append(id_time)

        for list_time in matching_ids:
            list_time_year = convert_timestamp_to_date(int(list_time[1]))
            if list_time_year[1] == datename_year[1]:
                id_id = list_time[0]
                return id_id
            else:
                id_id = "id错误"
                return id_id
        return


def fetch_limit_data_cls(datename, limit_type):
    url = ""
    date_times = convert_timestamp_to_date(datename)
    date = date_times[0]
    if limit_type == "午间涨停分析":
        # 填充你的涨停数据请求URL
        url = f"https://appsearch.cls.cn/api/search/get_all_list?app=cailianpress&sv=7.8.9&cuid=Unkown&os=android&ov=30&channel=6&type=telegram&province_code=6101&token=&uid=&mb=Xiaomi-M2102K1C&page=0&motif=0&rn=20&keyword={date}午间涨停分析"
    elif limit_type == "涨停分析":
        # 填充你的跌停数据请求URL
        url = f"https://appsearch.cls.cn/api/search/get_all_list?app=cailianpress&sv=7.8.9&cuid=Unkown&os=android&ov=30&channel=6&type=telegram&province_code=6101&token=&uid=&mb=Xiaomi-M2102K1C&page=0&motif=0&rn=20&keyword={date}涨停分析"
    elif limit_type == "连板股分析":
        # 填充你的跌停数据请求URL
        url = f"https://appsearch.cls.cn/api/search/get_all_list?app=cailianpress&sv=7.8.9&cuid=Unkown&os=android&ov=30&channel=6&type=telegram&province_code=6101&token=&uid=&mb=Xiaomi-M2102K1C&page=0&motif=0&rn=20&keyword={date}连板股分析"

    fetcher = DataFetcher_CLS()
    data = fetcher.fetch_data(url)

    if 'error' in data:
        return data['error']
    else:
        formatted_data = format_limit_data(data, limit_type, date_times)
        print(formatted_data)
        results = fetcher.get_url1(formatted_data)

        return results



# 在主线程中使用
if __name__ == "__main__":
    date = 1692691920  # 设置你的查询日期
    datename_year = convert_timestamp_to_date(date)

    limit_wjztfx_result = fetch_limit_data_cls(date, "午间涨停分析")
    limit_ztfx_result = fetch_limit_data_cls(date, "涨停分析")
    limit_lbgfx_result = fetch_limit_data_cls(date, "连板股分析")

    print(f"午间涨停分析======{limit_wjztfx_result}")
    print(f"涨停分析======{limit_ztfx_result}")
    print(f"连板股分析======{limit_lbgfx_result}")

    # with open("limit_data.txt", "w") as file:
    #     file.write(limit_up_result + "\n" + limit_down_result + "\n" + limit_lb_result + "\n" + limit_zb_result)

    # print("数据已写入到 limit_data.txt 文件中")



