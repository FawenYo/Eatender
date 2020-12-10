import sys

import requests

# 上層目錄import
sys.path.append(".")
from config import GOOGLE_MAPS_APIKEY


class GM_Restaurant:
    def __init__(self):
        self.restaurants = []

    def fetch_data(
        self, latitude, longitude, keyword, radius=2000, search_type="restaurant"
    ):
        """Google Maps 餐廳資料

        Args:
            latitude (float): 緯度
            longitude (float): 經度
            keyword (str): 關鍵字列表，以 " " 分割
            radius (int, optional): 限制範圍(單位：公尺). Defaults to 2000.
            search_type (str, optional): 限制類別. Defaults to "restaurant".
        """
        response = requests.get(
            f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?language=zh-TW&location={latitude},{longitude}&radius={radius}&type={search_type}&keyword={keyword}&key={GOOGLE_MAPS_APIKEY}"
        ).json()
        return self.parse_data(data=response)

    def parse_data(self, data):
        return data
