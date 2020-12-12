# ifood class object

import requests
from bs4 import BeautifulSoup

class Ifoodie:

    def __init__(self, user_search):
        self.user_search = user_search  # 欲搜尋的餐廳名稱，如"巷子口食堂"
        self.restaurant_url = self.restaurant_url()
        self.info = {
            "現正營業": str(),
            "店家地址": str(),
            "聯絡電話": str(),
            "均消價位": str()
        }
        self.get_info()
        self.comments = []
        self.get_comments()


    def restaurant_url(self):
        # 搜尋'台北公館站'附近的餐廳
        search_url = "https://ifoodie.tw/explore/list/" + \
                    self.user_search + \
                    "?poi=%E5%8F%B0%E5%8C%97%E5%85%AC%E9%A4%A8%E7%AB%99"

        response = requests.get(search_url)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")
        sel = str(soup.select("div.title a")).split(" ")
        for i in range(len(sel)):
            if "href=" in sel[i]:
                temp = sel[i].split("=")
                fragment_url = temp[1].strip("\"")
                break

        url = "https://ifoodie.tw" + fragment_url

        return (url)

    def get_info(self):
        response = requests.get(self.restaurant_url)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")
        sel = soup.select("div.jsx-558709029.info")

        temp_data = sel[0].text
        keys = list(self.info.keys())

        for i in range(len(keys)):
            if (i < len(keys) - 1 and
                    keys[i] in temp_data and
                    keys[i + 1] in temp_data):
                start = temp_data.find(keys[i]) + len(keys[i]) + 1
                end = temp_data.find(keys[i + 1])
                self.info[keys[i]] = temp_data[start:end].strip(" ")
            else:
                # to deal with avg. price
                start = temp_data.find(keys[i]) + len(keys[i]) + 1
                end = start + 10
                raw_string = temp_data[start:end]
                # sanitize raw string
                sanitize_candidate = []
                for m in range(len(raw_string)):
                    for n in range(m, len(raw_string)):
                        if raw_string[m:n].isdigit():
                            sanitize_candidate.append(raw_string[m:n].strip(" "))
                self.info[keys[i]] = max(sanitize_candidate)
    
    def get_comments(self):
        response = requests.get(self.restaurant_url)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")
        content_sel = soup.select("div.jsx-2738468548.message")

        for each in content_sel:
            self.comments.append(each.text)
