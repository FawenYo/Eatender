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
        self.comments = ""
        if request_review:
            self.comments = self.get_comments()

    def get_info(self) -> dict:
        # 將經緯度的精度限制在小數點後第5位之內，以便愛食記搜尋
        # 找到範圍1.5公里內的店家就好
        legal_name = self.restaurant_name.replace(" ", "%20")
        search_url = f"https://ifoodie.tw/explore/list/{legal_name}?range=1.5&latlng={self.latitude:.5f},{self.longitude:.5f}"
        response = requests.get(search_url, timeout=20)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")

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
            self.restaurant_url = "https://ifoodie.tw" + fragment_url
        except:
            self.restaurant_url = "https://ifoodie.tw"
            pass

        info = {
            "營業時間": "尚無營業時間資訊",
            "店家地址": "尚無店家地址資訊",
            "聯絡電話": "尚無聯絡電話資訊",
            "均消價位": "尚無均消價位資訊",
        }

        try:
            price_sel = soup.select("div.jsx-2133253768.avg-price")
            info["均消價位"] = re.findall(r"[0-9]+", str(price_sel[0]))[1]

            info_sel = soup.select("div.jsx-2133253768.info")
            operating_info = re.findall(
                r"</span>(.*)</div>", str(info_sel[0])
            )[0]
            temp = operating_info.split("營業:")
            info["營業時間"] = temp[1].strip(" ")

            address_sel = soup.select("div.jsx-2133253768.address-row")
            info["店家地址"] = re.findall(
                r"address-row\">(.*)</div>", str(address_sel[0])
            )[0]
        except:
            pass

        return info

    def get_comments(self) -> list:
        response = requests.get(self.restaurant_url, timeout=20)
        soup = BeautifulSoup(response.text, "html.parser")
        content_sel = soup.select("div.jsx-2738468548.message")

        comments = []
        for each in content_sel:
            comments.append(each.text)

        return comments
