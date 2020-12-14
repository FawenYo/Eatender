import sys
import threading

import requests

# 上層目錄import
sys.path.append(".")
from config import GOOGLE_MAPS_APIKEY, GOOGLE_MAPS_REQUEST_FIELD
from food.restaurant import Restaurant


class GM_Restaurant:
    def __init__(self):
        self.restaurants = []

    def fetch_data(
        self, latitude, longitude, keyword="", radius=2000, search_type="restaurant"
    ):
        """Google Maps 餐廳資料

        Args:
            latitude (float): 緯度
            longitude (float): 經度
            keyword (str): 關鍵字列表，以 " " 分割
            radius (int, optional): 限制範圍(單位：公尺). Defaults to 2000.
            search_type (str, optional): 限制類別. Defaults to "restaurant".
        """
        if keyword:
            response = requests.get(
                f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?language=zh-TW&location={latitude},{longitude}&radius={radius}&type={search_type}&keyword={keyword}&key={GOOGLE_MAPS_APIKEY}"
            ).json()
        else:
            response = requests.get(
                f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?language=zh-TW&location={latitude},{longitude}&radius={radius}&type={search_type}&key={GOOGLE_MAPS_APIKEY}"
            ).json()
        return self.parse_data(data=response)

    def parse_data(self, data):
        threads = []
        for place in data["results"][:6]:
            thread = threading.Thread(target=self.get_place_data, args=(place,))
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
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
            reviews = detail["reviews"]

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
