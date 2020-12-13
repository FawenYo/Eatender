import requests
from bs4 import BeautifulSoup


class Ifoodie:
    def __init__(self, restaurant_name, restaurant_address):
        self.restaurant_name = restaurant_name  # 欲搜尋的餐廳名稱，如"巷子口食堂"
        self.restaurant_address = restaurant_address
        self.restaurant_url = self.restaurant_url()
        self.info = self.get_info()
        self.comments = self.get_comments()

    def restaurant_url(self):
        # 搜尋'餐廳地址前三個字'附近的餐廳(待進一步修正)
        search_url = (
            "https://ifoodie.tw/explore/list/"
            + self.restaurant_name
            + "?poi="
            + self.restaurant_address[:3]
        )

        response = requests.get(search_url)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")
        sel = str(soup.select("div.title a")).split(" ")
        fragment_url = ""
        for i in range(len(sel)):
            if "href=" in sel[i]:
                temp = sel[i].split("=")
                fragment_url = temp[1].strip('"')
                break

        url = "https://ifoodie.tw" + fragment_url

        return url

    def get_info(self) -> dict:
        response = requests.get(self.restaurant_url)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")
        sel = soup.select("div.jsx-558709029.info")

        info = {
            "營業時間": str,
            "現正營業": str,  # temp
            "今日營業": str,  # temp
            "店家地址": str,
            "聯絡電話": str,
            "均消價位": str,
        }
        raw_info = sel[0].text
        keys = list(info.keys())

        for i in range(len(keys)):
            if i < len(keys) - 1 and keys[i] in raw_info and keys[i + 1] in raw_info:
                start = raw_info.find(keys[i]) + len(keys[i]) + 1
                end = raw_info.find(keys[i + 1])
                info[keys[i]] = raw_info[start:end].strip(" ")
            else:
                # 將均消的資訊分出來
                start = raw_info.find(keys[i]) + len(keys[i]) + 1
                end = start + 10
                raw_string = raw_info[start:end]
                rating_candidate = []
                for m in range(len(raw_string)):
                    for n in range(m, len(raw_string)):
                        if raw_string[m:n].isdigit():
                            rating_candidate.append(raw_string[m:n].strip(" "))
                info[keys[i]] = max(rating_candidate)

        # 取正確的時間到營業時間中
        if len(info["現正營業"]) > len(info["今日營業"]):
            info["營業時間"] = info["現正營業"]
        elif len(info["現正營業"]) < len(info["今日營業"]):
            info["營業時間"] = info["今日營業"]
        else:
            info["營業時間"] = "尚無營業時間資訊"

        info.pop("現正營業")
        info.pop("今日營業")
        return info

    def get_comments(self) -> list:
        response = requests.get(self.restaurant_url)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")
        content_sel = soup.select("div.jsx-2738468548.message")

        comments = []
        for each in content_sel:
            comments.append(each.text)

        return comments


print(Ifoodie("巷子口食堂", "台北市").__dict__)