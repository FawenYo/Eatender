import requests
import re
from bs4 import BeautifulSoup


class Ifoodie:
    def __init__(self, restaurant_name, latitude, longitude):
        self.restaurant_name = restaurant_name  # 欲搜尋的餐廳名稱，如"巷子口食堂"
        self.latitude = latitude
        self.longitude = longitude
        self.restaurant_url = self.restaurant_url()
        self.response = requests.get(self.restaurant_url)
        self.response.encoding = "utf-8"
        self.info = self.get_info()
        self.comments = self.get_comments()

    def restaurant_url(self):
        # 將經緯度的精度限制在小數點後第5位之內，以便愛食記搜尋
        # 找到範圍1.5公里內的店家就好
        search_url = f"https://ifoodie.tw/explore/list/{self.restaurant_name}?range=1.5&latlng={self.latitude:.5f},{self.longitude:.5f}"
        print(search_url)
        response = requests.get(search_url)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")

        # 找到範圍1.5公里內，第一家符合名稱的店家(搜尋順序是愛食記的搜尋結果)
        sel = soup.select("a.jsx-2133253768.title-text")
        fragment_url = ""
        for each in sel:
            if self.restaurant_name in each.text:
                fragment_url = re.findall(r'href=\"(.*)\" target', str(each))[0]
                break
        url = "https://ifoodie.tw" + fragment_url

        return url

    def get_info(self) -> dict:
        soup = BeautifulSoup(self.response.text, "html.parser")
        sel = soup.select("div.jsx-558709029.info")

        info = {
            "營業": "尚無營業時間資訊",  # temp
            "店家地址": "尚無店家地址資訊",
            "聯絡電話": "尚無聯絡電話資訊",
            "均消價位": "尚無均消價位資訊",
        }
        raw_info = sel[0].text
        keys = list(info.keys())

        for i in range(len(keys)):
            if keys[i] in raw_info:
                start = raw_info.find(keys[i]) + len(keys[i]) + 1
                next_keyword_index = -1
                for j in range(len(keys)):
                    if i < j and keys[j] in raw_info[start:]:
                        next_keyword_index = raw_info.find(keys[j])
                        break

                if next_keyword_index != -1:
                    info[keys[i]] = raw_info[start:next_keyword_index].strip("")
                else:
                    if keys[i] == "聯絡電話":
                        phone_candidate = []
                        raw_string = raw_info[start:]
                        for m in range(len(raw_string)):
                            for n in range(m, len(raw_string)):
                                if raw_string[m:n].isdigit():
                                    phone_candidate.append(raw_string[m:n].strip(" "))
                        info[keys[i]] = max(phone_candidate, key=len)

                    elif keys[i] == "均消價位":
                        rating_candidate = []
                        raw_string = raw_info[start:]
                        for m in range(len(raw_string)):
                            for n in range(m, len(raw_string)):
                                if raw_string[m:n].isdigit():
                                    rating_candidate.append(raw_string[m:n].strip(" "))
                        info[keys[i]] = max(rating_candidate, key=len)

        # 取正確的時間到營業時間中
        info["營業時間"] = info.pop("營業")

        return info

    def get_comments(self) -> list:
        soup = BeautifulSoup(self.response.text, "html.parser")
        content_sel = soup.select("div.jsx-2738468548.message")

        comments = []
        for each in content_sel:
            comments.append(each.text)

        return comments
