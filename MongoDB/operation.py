import sys
from datetime import datetime

import pytz

sys.path.append(".")
from config import db


def new_user(user_id: str):
    now = datetime.now(tz=pytz.timezone("Asia/Taipei"))
    data = {"user_id": user_id, "add_time": now, "favorite": []}
    db.user.insert_one(data)


def delete_user(user_id: str):
    db.user.delete_one({"user_id": user_id})


def record_user_location(user_id: str, lat: float, lng: float):
    now = datetime.now(tz=pytz.timezone("Asia/Taipei"))
    data = {
        "user_id": user_id,
        "location": [lat, lng],
        "time": now,
    }
    db.history.insert_one(data)


def add_restaurant(restaurant):
    now = datetime.now(tz=pytz.timezone("Asia/Taipei"))
    if not db.restaurant.find_one({"name": restaurant.name}):
        data = {
            "place_id": restaurant.place_id,
            "name": restaurant.name,
            "photo_url": restaurant.photo_url,
            "operating_time": restaurant.operating_time,
            "location": restaurant.location,
            "address": restaurant.address,
            "rating": restaurant.rating,
            "website": restaurant.website,
            "price": restaurant.price,
            "phone_number": restaurant.phone_number,
            "reviews": restaurant.reviews,
            "ifoodie_url": restaurant.ifoodie_url,
            "time": now,
        }
        db.restaurant.insert_one(data)
