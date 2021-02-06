import sys
import threading

import requests

sys.path.append(".")
import config
from food.model import Restaurant


class GoogleMaps:
    def __init__(
        self,
        latitude: float = 0.0,
        longitude: float = 0.0,
        keyword: str = "",
        search_type: str = "restaurant",
        complete_mode: bool = False,
        page_token: str = "",
        index: int = 0,
    ):
        """初始化

        Args:
            latitude (float): 使用者緯度. Defaults to 0.0.
            longitude (float): 使用者經度. Defaults to 0.0.
            keyword (str): 餐廳關鍵字列表，以 " " 分割.
            search_type (str, optional): 搜尋結果類別. Defaults to "restaurant".
            complete_mode(bool): 限制搜尋. Defaults to false.
            page_token (str, optional): 頁面搜尋token. Defaults to "".
            index (int, optional): 搜尋項目. Defaults to 0.
        """
        self.restaurants = []
        self.threads = []
        self.next_page = ""

        self.latitude = latitude
        self.longitude = longitude
        self.keyword = keyword
        self.search_type = search_type
        self.complete_mode = complete_mode
        self.current_page = page_token
        self.index = index

    def search_info(self, query: str):
        """搜尋餐廳名稱

        Args:
            query (str): 餐廳名稱
        """
        param_data = {
            "language": "zh-TW",
            "query": query,
            "key": config.GOOGLE_MAPS_APIKEY,
        }
        response = requests.get(
            f"https://maps.googleapis.com/maps/api/place/textsearch/json",
            params=param_data,
        )
        return self.parse_data(data=response.json())

    def nearby_info(self, page_token: str):
        """搜尋附近餐廳

        Args:
            page_token (str): Google Maps page token.
        """
        radius = 1000 if not self.complete_mode else 50000
        param_data = {
            "language": "zh-TW",
            "location": f"{self.latitude},{self.longitude}",
            "radius": radius,
            "type": self.search_type,
            "keyword": self.keyword,
            "pagetoken": page_token,
            "key": config.GOOGLE_MAPS_APIKEY,
        }
        response = requests.get(
            f"https://maps.googleapis.com/maps/api/place/nearbysearch/json",
            params=param_data,
        )
        return self.parse_data(data=response.json())

    def parse_data(self, data):
        """處理Google Maps 回傳結果

        Args:
            data (json): Google Maps 搜尋結果
        """
        if not self.complete_mode:  # 非完整模式只取5個
            filter_results = data["results"][0 + 5 * self.index : 5 + 5 * self.index]
        else:
            filter_results = data["results"]

        for place in filter_results:
            # 取得餐廳資訊
            thread = threading.Thread(target=self.get_place_data, args=(place,))
            self.threads.append(thread)

        if not self.complete_mode:
            if len(data["results"][5 + 5 * self.index :]) > 0:
                self.next_page = f"{self.current_page}[|]{self.index + 1}"
            elif "next_page_token" in data:
                self.next_page = f"{data['next_page_token']}[|]0"
            self.start_thread()
        # 搜尋完畢
        elif "next_page_token" not in data:
            self.start_thread()
        # 完整搜尋
        else:
            self.nearby_info(page_token=data["next_page_token"])

    def start_thread(self):
        # 使用多線程方式取得所有餐廳資訊
        for thread in self.threads:
            thread.start()

        for thread in self.threads:
            thread.join()

    def get_place_data(self, place):
        """取得餐廳資訊

        Args:
            place (json dict): 餐廳資料
        """
        place_id = place["place_id"]
        if "opening_hours" not in place:
            open_now = False
        else:
            open_now = place["opening_hours"]["open_now"]

        data = config.db.restaurant.find_one({"place_id": place_id})
        # 資料已存在於資料庫 (避免浪費使用 Google Maps Token)
        if data:
            self.load_from_database(place_id=place_id, open_now=open_now, data=data)
        else:
            self.load_from_google(place_id=place_id, open_now=open_now, place=place)

    def place_detail(self, place_id: str):
        """取得餐廳 Google Maps 詳細資訊

        Args:
            place_id (str): 餐廳 Google Maps place id

        Returns:
            json: 餐廳詳細資訊
        """
        fileds_data = ",".join(config.GOOGLE_MAPS_REQUEST_FIELD)
        response = requests.get(
            f"https://maps.googleapis.com/maps/api/place/details/json?language=zh-TW&place_id={place_id}&fields={fileds_data}&key={config.GOOGLE_MAPS_APIKEY}"
        ).json()
        return response["result"]

    def place_photo(self, photo_reference: str, max_width: int = 400) -> str:
        """餐廳 Google Maps 照片

        Args:
            photo_reference (str): Google Maps photo_reference.
            max_width (int, optional): 照片寬度. Defaults to 400.

        Returns:
            str: 餐廳照片網址
        """
        photo_url = requests.get(
            f"https://maps.googleapis.com/maps/api/place/photo?maxwidth={max_width}&photoreference={photo_reference}&key={config.GOOGLE_MAPS_APIKEY}"
        ).url
        return photo_url

    def load_from_database(self, place_id: str, open_now: bool, data: dict):
        """從資料庫中取得餐廳資訊

        Args:
            place_id (str): 餐廳 Google Maps place id
            open_now (bool): 餐廳營業狀況
            data (dict): 餐廳資料
        """
        name = data["name"]
        photo_url = data["photo_url"]
        operating_time = data["operating_time"]
        location = data["location"]
        address = data["address"]
        rating = data["rating"]
        website = data["website"]
        google_url = data["google_url"]
        phone_number = data["phone_number"]
        reviews = data["reviews"]
        restaurant = Restaurant(
            place_id=place_id,
            name=name,
            photo_url=photo_url,
            open_now=open_now,
            operating_time=operating_time,
            location=location,
            address=address,
            rating=rating,
            website=website,
            google_url=google_url,
            phone_number=phone_number,
            reviews=reviews,
        )
        self.restaurants.append(restaurant)

    def load_from_google(self, place_id: str, open_now: bool, place):
        """從 Google Maps 取得餐廳資訊

        Args:
            place_id (str): 餐廳 Google Maps place id
            open_now (bool): 餐廳營業狀況
            place (json dict): 餐廳資料
        """
        try:
            detail = self.place_detail(place_id=place_id)
            photo_reference = place["photos"][0]["photo_reference"]
            photo_url = self.place_photo(photo_reference=photo_reference)
            name = place["name"]
            location = place["geometry"]["location"]
            rating = place["rating"]
            if "opening_hours" not in detail:
                operating_time = {
                    "open_now": False,
                    "periods": [],
                    "weekday_text": [
                        "星期一: 休息",
                        "星期二: 休息",
                        "星期三: 休息",
                        "星期四: 休息",
                        "星期五: 休息",
                        "星期六: 休息",
                        "星期日: 休息",
                    ],
                }
            else:
                operating_time = detail["opening_hours"]
            address = detail["formatted_address"]
            phone_number = detail["formatted_phone_number"]
            if "website" in detail:
                website = detail["website"]
            elif "url" in place:
                website = place["url"]
            else:
                website = "https://www.google.com.tw/maps"
            google_url = detail["url"]
            reviews = []
            for each in detail["reviews"]:
                content = each["text"]
                reviews.append(content)

            restaurant = Restaurant(
                place_id=place_id,
                name=name,
                photo_url=photo_url,
                open_now=open_now,
                operating_time=operating_time,
                location=location,
                address=address,
                rating=rating,
                website=website,
                google_url=google_url,
                phone_number=phone_number,
                reviews=reviews,
            )
            self.restaurants.append(restaurant)
        except KeyError:
            config.console.print_exception()