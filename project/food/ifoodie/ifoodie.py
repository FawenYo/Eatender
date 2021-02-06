import re

import requests
from bs4 import BeautifulSoup


class Ifoodie:
    def __init__(self, restaurant_name: str, latitude: float, longitude: float):
        """Initial Ifoodie info

        Args:
            restaurant_name (str): 欲搜尋的餐廳名稱，如"巷子口食堂"
            latitude (float): 餐廳經度
            longitude (float): 餐廳緯度
        """
        self.restaurant_name = restaurant_name
        self.latitude = latitude
        self.longitude = longitude
        self.restaurant_url, self.price = self.get_ifoodie_info()

    def get_ifoodie_info(self) -> tuple:
        # 將經緯度的精度限制在小數點後第5位之內，以便愛食記搜尋
        # 找到範圍1.5公里內的店家就好
        legal_name = self.restaurant_name.replace(" ", "%20")
        search_url = f"https://ifoodie.tw/explore/list/{legal_name}?range=1.5&latlng={self.latitude:.5f},{self.longitude:.5f}"
        response = requests.get(search_url, timeout=20)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")

        # 愛食記網址
        try:
            url_sel = soup.select("a.jsx-2133253768.title-text")
            if not url_sel:
                legal_name = legal_name.split("-")[0]
                search_url = f"https://ifoodie.tw/explore/list/{legal_name}?range=1.5&latlng={self.latitude:.5f},{self.longitude:.5f}"
                response = requests.get(search_url, timeout=20)
                response.encoding = "utf-8"
                soup = BeautifulSoup(response.text, "html.parser")
                url_sel = soup.select("a.jsx-2133253768.title-text")
            fragment_url = re.findall(r"href=\"(.*)\" target", str(url_sel[0]))[0]
            restaurant_url = "https://ifoodie.tw" + fragment_url
        except:
            restaurant_url = "https://ifoodie.tw"
            pass

        # 均消價位
        try:
            price_sel = soup.select("div.jsx-2133253768.avg-price")
            price = re.findall(r"[0-9]+", str(price_sel[0]))[1]
        except:
            price = 0
        return restaurant_url, price
