import random
import re
import string
import sys
import threading
from datetime import datetime, timedelta

from .google_maps.info import GM_Restaurant
from .ifoodie.ifoodie import Ifoodie

sys.path.append(".")
from bson.son import SON
from pymongo import GEOSPHERE

import config
import MongoDB.operation as database


class Restaurant_Info:
    def __init__(
        self, latitude: float = 0.0, longitude: float = 0.0, keyword="", page_token=""
    ):
        self.restaurants = []
        self.next_page = ""
        self.latitude = latitude
        self.longitude = longitude
        self.keyword = keyword
        self.page_token = page_token

    def search(self, query: str):
        threads = []
        self.google_maps_search(query=query)
        self.get_ifoodie_data()
        # Add to MongoDB
        for restaurant in self.restaurants:
            thread = threading.Thread(
                target=database.add_restaurant, args=(restaurant, self.keyword)
            )
            threads.append(thread)
        for thread in threads:
            thread.start()

    def nearby(self):
        # Get nearby restaurants
        threads = []
        self.google_maps_nearby()
        self.get_ifoodie_data()
        # Load from database
        """ result = []
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
                        ("$maxDistance", 1000),
                    ]
                )
            },
            "category": self.keyword,
        }
        for each in config.db.restaurant.find(query):
            result.append(each)
        if len(result) >= 5:
            print("load from db.")
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
                    google_url=each["google_url"],
                    phone_number=each["phone_number"],
                    reviews=each["reviews"],
                )
                self.restaurants.append(restaurant)
        else:
            self.get_google_maps_data()
            self.get_ifoodie_data() """
        # Add to MongoDB
        for restaurant in self.restaurants:
            thread = threading.Thread(
                target=database.add_restaurant, args=(restaurant, self.keyword)
            )
            threads.append(thread)
        for thread in threads:
            thread.start()

    def google_maps_search(self, query: str):
        restaurants = GM_Restaurant()
        restaurants.search_info(query=query)
        self.next_page = restaurants.next_page
        if self.next_page:
            token_table = config.db.page_token.find_one({})
            if self.next_page not in token_table["data"].values():
                token_key = "".join(
                    random.choice(string.ascii_letters + string.digits)
                    for x in range(10)
                )
                token_table["data"][token_key] = self.next_page
                config.db.page_token.update_one({}, {"$set": token_table})
                self.next_page = token_key
            else:
                for key, value in token_table["data"].items():
                    if value == self.next_page:
                        self.next_page = key
        self.restaurants = restaurants.restaurants

    def google_maps_nearby(self, complete_mode=False):
        """Get Google Maps nearby restaurants data

        Args:
            complete_mode (bool, optional): Set it to True to get complete data. Defaults to False.
        """
        if "[|]" not in self.page_token:
            page_token = self.page_token
            index = 0
        else:
            page_token, index = self.page_token.split("[|]")
        restaurants = GM_Restaurant(
            latitude=self.latitude,
            longitude=self.longitude,
            keyword=self.keyword,
            complete_mode=complete_mode,
            page_token=page_token,
            index=int(index),
        )
        restaurants.nearby_info(page_token=page_token)
        if not complete_mode:
            self.next_page = restaurants.next_page
            if self.next_page:
                token_table = config.db.page_token.find_one({})
                if self.next_page not in token_table["data"].values():
                    token_key = "".join(
                        random.choice(string.ascii_letters + string.digits)
                        for x in range(10)
                    )
                    token_table["data"][token_key] = self.next_page
                    config.db.page_token.update_one({}, {"$set": token_table})
                    self.next_page = token_key
                else:
                    for key, value in token_table["data"].items():
                        if value == self.next_page:
                            self.next_page = key
            self.restaurants = restaurants.restaurants
        else:
            return restaurants

    def get_ifoodie_data(self, restaurants: object = object, complete_mode=False):
        """Get ifoodie data

        Args:
            restaurants (object, optional): Restaurants data. Defaults to object.
            complete_mode (bool, optional): Set it to True to get complete data. Defaults to False.

        Returns:
            [type]: [description]
        """
        threads = []
        if not complete_mode:
            for restaurant in self.restaurants:
                config.restaurants[restaurant.place_id] = restaurant.__dict__
                thread = threading.Thread(
                    target=self.multi_threading_ifoodie, args=(restaurant,)
                )
                threads.append(thread)
        else:
            for restaurant in restaurants.restaurants:
                config.restaurants[restaurant.place_id] = restaurant.__dict__
                thread = threading.Thread(
                    target=self.multi_threading_ifoodie, args=(restaurant,)
                )
                threads.append(thread)

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        if complete_mode:
            return restaurants

    def multi_threading_ifoodie(self, restaurant: object):
        """Multi-threading Get ifoodie data

        Args:
            restaurant (object): Restaurant data
        """
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


# 店家營業狀態
def find_operating_status(data):
    now = datetime.now()
    today_date = now.strftime("%Y:%m:%d")
    time = now.strftime("%H:%M")

    today_open = data[now.weekday()].split(",")
    for each in today_open:
        if "休息" in each:
            return False
        if "24 小時營業" in each:
            return False
        temp = re.findall(r"\d{1,2}\:\d{1,2}", each)
        start = datetime.strptime(f"{today_date}:{temp[0]}", "%Y:%m:%d:%H:%M")
        current = datetime.strptime(f"{today_date}:{time}", "%Y:%m:%d:%H:%M")
        end = datetime.strptime(f"{today_date}:{temp[1]}", "%Y:%m:%d:%H:%M")
        if int(temp[0][0:2]) > int(temp[1][0:2]):
            end += timedelta(days=1)

        if start <= current <= end:
            return True
    return False
