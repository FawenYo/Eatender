import re
import sys
import threading
from datetime import datetime

from .google_maps.info import GM_Restaurant
from .ifoodie.ifoodie import Ifoodie
from .restaurant import Restaurant

# 上層目錄import
sys.path.append(".")
from bson.son import SON
from pymongo import GEOSPHERE

import config
import MongoDB.operation as database


class Nearby_restaurant:
    def __init__(self, latitude, longitude, keyword=""):
        self.restaurants = []
        self.latitude = latitude
        self.longitude = longitude
        self.keyword = keyword
        self.get_info()

    def get_info(self):
        result = []
        config.db.restaurant.create_index([("loc", GEOSPHERE)])
        query = {
            "loc": {
                "$near": SON(
                    [
                        (
                            "$geometry",
                            SON(
                                [
                                    ("type", "Point"),
                                    ("coordinates", [self.longitude, self.latitude]),
                                ]
                            ),
                        ),
                        ("$maxDistance", 2000),
                    ]
                )
            },
            "category": self.keyword,
        }
        for each in config.db.restaurant.find(query):
            result.append(each)
        if len(result) >= 5:
            for each in result:
                restaurant = Restaurant(
                    place_id=each["place_id"],
                    name=each["name"],
                    photo_url=each["photo_url"],
                    open_now=find_operating_status(
                        data=each["operating_time"]["weekday_text"]
                    ),
                    operating_time=each["operating_time"],
                    location=each["location"],
                    address=each["address"],
                    rating=each["rating"],
                    website=each["website"],
                    phone_number=each["phone_number"],
                    reviews=each["reviews"],
                )
                self.restaurants.append(restaurant)
        else:
            self.get_google_maps_data()
            self.get_ifoodie_data()
        # Updating Silently
        thread = threading.Thread(target=self.silent_update)
        thread.start()

    def get_google_maps_data(self):
        restaurants = GM_Restaurant()
        restaurants.fetch_data(
            latitude=self.latitude, longitude=self.longitude, keyword=self.keyword
        )
        self.restaurants = restaurants.restaurants

    def get_ifoodie_data(self):
        for restaurant in self.restaurants:
            try:
                data = Ifoodie(
                    restaurant_name=restaurant.name,
                    latitude=self.latitude,
                    longitude=self.longitude,
                )
                restaurant.ifoodie_url = data.restaurant_url
                restaurant.price = int(data.info["均消價位"])
                restaurant.reviews += data.comments
            except ValueError:
                pass
            except IndexError:
                pass

    def silent_update(self):
        threads = []
        # Google Maps
        restaurants = GM_Restaurant(speed_mode=False)
        restaurants.fetch_data(
            latitude=self.latitude,
            longitude=self.longitude,
            keyword=self.keyword,
        )
        # Ifoodie
        for restaurant in restaurants.restaurants:
            try:
                data = Ifoodie(
                    restaurant_name=restaurant.name,
                    latitude=self.latitude,
                    longitude=self.longitude,
                )
                restaurant.ifoodie_url = data.restaurant_url
                restaurant.price = int(data.info["均消價位"])
                restaurant.reviews += data.comments
            except ValueError:
                pass
            except IndexError:
                pass
        # Add to MongoDB
        for restaurant in self.restaurants:
            thread = threading.Thread(
                target=database.add_restaurant, args=(restaurant, self.keyword)
            )
            threads.append(thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        print("Silent update done.")


def find_operating_status(data):
    now = datetime.now()
    weekday = now.weekday()
    time = now.strftime("%H:%M")

    today_open = data[weekday - 1].split(",")
    for each in today_open:
        if "休息" in each:
            return False
        temp = re.findall(r"\d{2}\:\d{2}", each)
        start = datetime.strptime(temp[0], "%H:%M")
        end = datetime.strptime(temp[1], "%H:%M")
        current = datetime.strptime(time, "%H:%M")

        if start <= current <= end:
            return True
    return False
