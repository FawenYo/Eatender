import re
import sys
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup


class Weather:
    def __init__(self):
        self.location_name: str = ""
        # 風向，單位 度，一般風向 0 表示無風
        self.wind_direction: str = ""
        # 風速，單位 公尺/秒
        self.wind_speed: int = 0
        # 小時最大陣風風速，單位 公尺/秒
        self.h_fx: int = 0
        # 溫度，單位 攝氏
        self.temperature: int = 0
        # 最高溫度
        self.max_temperature: int = 0
        # 最低溫度
        self.min_temperature: int = 0
        # 相對濕度，單位 百分比率
        self.humidity: int = 0
        # 日累積雨量，單位 毫米
        self.rain: int = 0
        # 紫外線強度
        self.uvi: int = 0
        # 天氣描述 (中文)
        self.wx: str = ""
        # 空氣品質
        self.aqi: int = 0

    def fetch_data(self, lat, lng):
        """抓取天氣資料

        Args:
            lat (float): 緯度
            lng (float): 經度

        Data Source:
            app.wemega.tw: "天氣即時預報" App
        """
        response = requests.get(f"https://app.wmega.tw/v1/all/{lat}/{lng}").json()
        return self.parse_data(data=response)

    def parse_data(self, data):
        """解析資料

        Args:
            data (JSON): 天氣資料內容
        """
        self.location_name = data["now"]["name"]
        self.wind_direction = data["now"]["wdir"]
        self.wind_speed = data["now"]["wdsd"]
        self.h_fx = data["now"]["h_fx"]
        self.temperature = data["now"]["temp"]
        self.humidity = data["now"]["humd"]
        self.rain = data["now"]["h24r"]
        self.uvi = data["now"]["uviValue"]
        self.max_temperature = data["now"]["maxT"]
        self.min_temperature = data["now"]["minT"]
        self.wx = data["now"]["wx"]
        self.aqi = data["aqi"]["content"]["aqiValue"]

    def customized_category(self, lat, lng) -> dict:
        """依照天氣、日期，動態的新增類別

        Args:
            lat (float): 緯度
            lng (float): 經度
        """
        self.fetch_data(lat=lat, lng=lng)

        category_reference = {
            "好冷，想來點...": "火鍋",
            "好熱，想來點...": "冰品",
            "週末假期，想來點...": "聚餐",
            "這麼晚了，想來點...": "宵夜",
            "情人節，想來點...": "聚餐",
            "農曆新年，想來點...": "聚餐",
            "元宵節，想來點...": "湯圓",
            "端午節，想來點...": "粽子",
            "中秋節，想來點...": "烤肉",
            "冬至，想來點...": "湯圓",
        }

        def add_to_customized(keyword: str):
            for category in category_reference.keys():
                if keyword in category:
                    customized_category[category] = category_reference[category]
                    break

        customized_category = {}

        if self.temperature >= 25 or self.max_temperature >= 25:
            add_to_customized(keyword="好熱")
        elif self.temperature <= 20 or self.min_temperature <= 25:
            add_to_customized(keyword="好冷")

        # 判斷是否今天是否為節日前後
        today = datetime.now()
        response = requests.get(f"https://toolskk.com/{today.year}calendar", timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        festivals = {
            "農曆新年": re.findall("(\d{1,2}/\d{1,2}) 除夕過年", soup.text),
            "情人節": re.findall("(\d{1,2}/\d{1,2}).*?情人節", soup.text),
            "端午節": re.findall("(\d{1,2}/\d{1,2}) 端午節", soup.text),
            "中秋節": re.findall("(\d{1,2}/\d{1,2}) 中秋節", soup.text),
            "元宵節": re.findall("(\d{1,2}/\d{1,2}) 元宵節", soup.text),
            "冬至": re.findall("(\d{1,2}/\d{1,2}) 冬至", soup.text),
        }

        for festival, period in festivals.items():

            if len(period) == 1:
                if festival == "農曆新年":
                    start = datetime.strptime(f"{today.year}/{period[0]}", "%Y/%m/%d")
                    end = start + timedelta(days=7)

                    if start <= today <= end:
                        add_to_customized(keyword=festival)
                elif festival == "中秋節":
                    base = datetime.strptime(f"{today.year}/{period[0]}", "%Y/%m/%d")
                    start = base - timedelta(days=15)
                    end = base + timedelta(days=15)
                    if start <= today <= end:
                        add_to_customized(keyword=festival)
                else:
                    start = datetime.strptime(f"{today.year}/{period[0]}", "%Y/%m/%d")
                    if start == today:
                        add_to_customized(keyword=festival)
            else:
                for each in period:
                    if festival == "情人節":
                        end = datetime.strptime(f"{today.year}/{each}", "%Y/%m/%d")
                        start = end - timedelta(days=3)
                        if start <= today <= end:
                            add_to_customized(keyword=festival)

        return customized_category
