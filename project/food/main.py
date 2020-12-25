import random
import re
import string
import sys
import threading
from datetime import datetime

from .google_maps.info import GM_Restaurant
from .ifoodie.ifoodie import Ifoodie
from .restaurant import Restaurant

# 上層目錄import
sys.path.append(".")
import config
import MongoDB.operation as database
from bson.son import SON
from pymongo import GEOSPHERE


class Nearby_restaurant:
    def __init__(self, latitude, longitude, keyword="", page_token=""):
        self.restaurants = []
        self.next_page = ""
        self.latitude = latitude
        self.longitude = longitude
        self.keyword = keyword
        self.page_token = page_token
        self.get_info()

    def get_info(self):
        threads = []
        self.get_google_maps_data()
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

        # Updating Silently
        thread = threading.Thread(target=self.silent_update)
        thread.start()

    def get_google_maps_data(self, complete_mode=False):
        restaurants = GM_Restaurant(
            latitude=self.latitude,
            longitude=self.longitude,
            keyword=self.keyword,
            complete_mode=complete_mode,
            page_token=self.page_token,
        )
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
                    for key, value in token_table[
                        "data"
                    ].items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
                        if value == self.next_page:
                            self.next_page = key
            self.restaurants = restaurants.restaurants
        else:
            return restaurants

    def get_ifoodie_data(self, complete_mode=False, restaurants=object):
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

    def multi_threading_ifoodie(self, restaurant):
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
        restaurants = self.get_google_maps_data(complete_mode=True)
        restaurants = self.get_ifoodie_data(complete_mode=True, restaurants=restaurants)
        # Add to MongoDB
        for restaurant in restaurants.restaurants:
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

    today_open = data[weekday].split(",")
    for each in today_open:
        if "休息" in each:
            return False
        temp = re.findall(r"\d{1,2}\:\d{1,2}", each)
        start = datetime.strptime(f"{temp[0]}:{str(weekday)}", "%H:%M:%d")
        current = datetime.strptime(f"{time}:{str(weekday)}", "%H:%M:%d")
        if int(temp[0][0:2]) <= int(temp[1][0:2]):
            end = datetime.strptime(f"{temp[1]}:{str(weekday)}", "%H:%M:%d")
        else:
            end = datetime.strptime(f"{temp[1]}:{str(weekday + 1)}", "%H:%M:%d")

        if start <= current <= end:
            return True
    return False
