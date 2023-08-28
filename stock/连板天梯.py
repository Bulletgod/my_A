#!/usr/bin/env python
# coding:utf-8
# @time: 2023/8/22 13:45
# @softaware:PyCharm
# 学习从0-1

import requests


class DataFetcher_LBTT:
    def __init__(self):
        self.url = "https://data.10jqka.com.cn/dataapi/limit_up/continuous_limit_up?filter=HS,GEM2STAR&date="
        self.headers = {
            'Sec-Ch-Ua-Platform': 'Android',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36'
        }

    def fetch_data(self, date):
        try:
            response = requests.get(self.url + date, headers=self.headers)
            response_json = response.json()

            if response_json.get("status_code") == 0:
                formatted_output = f"连板天梯\n当前查询日期：{date}\n"

                for entry in response_json["data"]:
                    formatted_output += f"高度：{entry['height']}\n"
                    if "code_list" in entry:
                        codes = ", ".join([f"{code_entry['code']} {code_entry['name']}" for code_entry in entry["code_list"]])
                        formatted_output += codes + "\n"

                return formatted_output
            else:
                return "接口返回异常。"
        except Exception as e:
            return "发生异常：" + str(e)


# 在主线程中使用
if __name__ == "__main__":
    fetcher = DataFetcher_LBTT()

    date = "20230821"  # 设置你的查询日期
    result = fetcher.fetch_data(date)
    print(result)
