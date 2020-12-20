import sys

import requests

# 上層目錄import
sys.path.append(".")


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
