import re

import requests
from bs4 import BeautifulSoup


class Ifoodie:
    def __init__(self, restaurant_name, latitude, longitude, request_review=False):
        self.restaurant_name = restaurant_name  # 欲搜尋的餐廳名稱，如"巷子口食堂"
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.restaurant_url = str()
        self.info = self.get_info()
        if request_review:
            self.comments = self.get_comments()

    def get_info(self) -> dict:
        # 將經緯度的精度限制在小數點後第5位之內，以便愛食記搜尋
        # 找到範圍1.5公里內的店家就好
        search_url = f"https://ifoodie.tw/explore/list/{self.restaurant_name}?range=1.5&latlng={self.latitude:.5f},{self.longitude:.5f}"
        response = requests.get(search_url, timeout=20)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")

        # 找到範圍1.5公里內，第一家符合名稱的店家(搜尋順序是愛食記的搜尋結果)
        url_sel = soup.select("a.jsx-2133253768.title-text")
        fragment_url = ""
        target_index = int()
        for i in range(len(url_sel)):
            if self.restaurant_name in url_sel[i].text:
                fragment_url = re.findall(r"href=\"(.*)\" target", str(url_sel[i]))[0]
                target_index = i
                break
        self.restaurant_url = "https://ifoodie.tw" + fragment_url
        
        price_sel = soup.select("div.jsx-2133253768.avg-price")
        avg_price = re.findall(r"[0-9]+", str(price_sel[target_index]))[1]

        info = {
            "營業時間": "尚無營業時間資訊",
            "店家地址": "尚無店家地址資訊",
            "聯絡電話": "尚無聯絡電話資訊",
            "均消價位": str(avg_price),
        }
        return info

    def get_comments(self) -> list:
        response = requests.get(self.restaurant_url, timeout=20)
        soup = BeautifulSoup(response.text, "html.parser")
        content_sel = soup.select("div.jsx-2738468548.message")

        comments = []
        for each in content_sel:
            comments.append(each.text)

        return comments
