import random
import sys
import threading

import requests

# 上層目錄import
sys.path.append(".")
from config import GOOGLE_MAPS_APIKEY, GOOGLE_MAPS_REQUEST_FIELD
from food.restaurant import Restaurant


class GM_Restaurant:
    def __init__(
        self,
        latitude: float,
        longitude: float,
        keyword: str = "",
        search_type: str = "restaurant",
        complete_mode=False,
        page_token="",
    ):
        """初始化

        Args:
            latitude (float): 緯度.
            longitude (float): 經度.
            keyword (str): 關鍵字列表，以 " " 分割.
            search_type (str, optional): 限制類別. Defaults to "restaurant".
            complete_mode(bool): 限制搜尋.
        """
        self.restaurants = []
        self.threads = []
        self.next_page = ""

        self.latitude = latitude
        self.longitude = longitude
        self.keyword = keyword
        self.search_type = search_type
        self.complete_mode = complete_mode

        self.fetch_data(pagetoken=page_token)

    def fetch_data(
        self,
        pagetoken: str = "",
    ):
        """Google Maps 餐廳資料

        Args:
            pagetoken (str): Google Maps search page token.

        """
        radius = 1000 if not self.complete_mode else 50000
        param_data = {
            "language": "zh-TW",
            "location": f"{self.latitude},{self.longitude}",
            "radius": radius,
            "type": self.search_type,
            "keyword": self.keyword,
            "pagetoken": pagetoken,
            "key": GOOGLE_MAPS_APIKEY,
        }
        response = requests.get(
            f"https://maps.googleapis.com/maps/api/place/nearbysearch/json",
            params=param_data,
        )
        return self.parse_data(data=response.json())

    def parse_data(self, data):
        if not self.complete_mode:
            if len(data["results"]) < 6:
                filter_results = data["results"]
            else:
                filter_results = random.sample(data["results"], 6)
        else:
            filter_results = data["results"]
        for place in filter_results:
            thread = threading.Thread(target=self.get_place_data, args=(place,))
            self.threads.append(thread)
        if not self.complete_mode or "next_page_token" not in data:
            if "next_page_token" in data:
                self.next_page = data["next_page_token"]
            self.start_thread()
        else:
            self.fetch_data(pagetoken=data["next_page_token"])

    def start_thread(self):
        for thread in self.threads:
            thread.start()

        for thread in self.threads:
            thread.join()

    def get_place_data(self, place):
        try:
            place_id = place["place_id"]
            detail = self.place_detail(place_id=place_id)
            photo_reference = place["photos"][0]["photo_reference"]
            photo_url = self.place_photo(photo_reference=photo_reference)
            name = place["name"]
            location = place["geometry"]["location"]
            open_now = place["opening_hours"]["open_now"]
            rating = place["rating"]
            operating_time = detail["opening_hours"]
            address = detail["formatted_address"]
            phone_number = detail["formatted_phone_number"]
            if "website" in detail:
                website = detail["website"]
            else:
                website = place["url"]
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
            pass

    def place_detail(self, place_id):
        fileds_data = ",".join(GOOGLE_MAPS_REQUEST_FIELD)
        response = requests.get(
            f"https://maps.googleapis.com/maps/api/place/details/json?language=zh-TW&place_id={place_id}&fields={fileds_data}&key={GOOGLE_MAPS_APIKEY}"
        ).json()
        return response["result"]

    def place_photo(self, photo_reference, max_width=400):
        photo_url = requests.get(
            f"https://maps.googleapis.com/maps/api/place/photo?maxwidth={max_width}&photoreference={photo_reference}&key={GOOGLE_MAPS_APIKEY}"
        ).url
        return photo_url
