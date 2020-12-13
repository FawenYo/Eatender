from datetime import datetime
import pytz
import sys

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
    data = {
        "name": restaurant.name,
        "photo_url": restaurant.photo_url,
        "operating_time": restaurant.operating_time,
        "location": restaurant.location,
        "address": restaurant.address,
        "rating": restaurant.rating,
        "phone_number": restaurant.phone_number,
        "reviews": restaurant.reviews,
        "time": now,
    }
    db.restaurant.insert_one(data)