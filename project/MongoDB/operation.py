import sys
import random
import string
from datetime import datetime

import pytz

sys.path.append(".")
from config import db


def new_user(user_id: str, display_name: str):
    """LINE Bot - New User

    Args:
        user_id (str): LINE User ID
        display_name (str): LINE User Name
    """
    now = datetime.now(tz=pytz.timezone("Asia/Taipei"))
    data = {
        "user_id": user_id,
        "display_name": display_name,
        "add_time": now,
        "favorite": [],
        "vote": [],
        "notify": {"status": False, "token": ""},
    }
    db.user.insert_one(data)


def delete_user(user_id: str):
    """LINE Bot - Delete User

    Args:
        user_id (str): LINE User ID
    """
    db.user.delete_one({"user_id": user_id})


def record_user_search(user_id: str, lat: float, lng: float, search: str):
    """LINE Bot - Record user

    Args:
        user_id (str): LINE User ID
        lat (float): Location latitude
        lng (float): Location longitude
        search (str): Search Texts
    """
    now = datetime.now(tz=pytz.timezone("Asia/Taipei"))
    if search == "":
        search = "隨便"
    data = {
        "user_id": user_id,
        "location": [lat, lng],
        "search": search,
        "time": now,
    }
    db.history.insert_one(data)


def add_restaurant(restaurant: object, keyword: str):
    """New restaurant

    Args:
        restaurant (object): Restaurant data (food/model.py)
        keyword (str): Restaurant category
    """
    now = datetime.now(tz=pytz.timezone("Asia/Taipei"))
    result = db.restaurant.find_one({"name": restaurant.name})
    if not result:
        data = {
            "place_id": restaurant.place_id,
            "name": restaurant.name,
            "photo_url": restaurant.photo_url,
            "operating_time": restaurant.operating_time,
            "location": restaurant.location,
            "loc": [restaurant.location["lng"], restaurant.location["lat"]],
            "address": restaurant.address,
            "rating": restaurant.rating,
            "website": restaurant.website,
            "google_url": restaurant.google_url,
            "price": restaurant.price,
            "phone_number": restaurant.phone_number,
            "reviews": restaurant.reviews,
            "keywords": restaurant.keywords,
            "ifoodie_url": restaurant.ifoodie_url,
            "category": [],
            "time": now,
        }
        if keyword:
            data["category"].append(keyword)
        db.restaurant.insert_one(data)
    else:
        if keyword not in result["category"]:
            result["category"].append(keyword)
            db.restaurant.update_one({"name": restaurant.name}, {"$set": result})


def create_vote(
    creator: str, vote_id: str, vote_link: str, restaurants: list, end_date: datetime
):
    """Create vote event

    Args:
        creator (str): Creator's LINE User ID
        vote_id (str): Vote's event ID
        vote_link (str): When2meet link
        restaurants (list): Restaurant list
        end_date (datetime): Vote end date
    """
    now = datetime.now(tz=pytz.timezone("Asia/Taipei"))
    if not db.vote_pull.find_one({"_id": vote_id}):
        data = {
            "_id": vote_id,
            "creator": creator,
            "vote_link": vote_link,
            "end_date": end_date,
            "restaurants": restaurants,
            "create_time": now,
            "participants": {},
        }
        db.vote_pull.insert_one(data)


def create_vote_event(param):
    now = datetime.now(tz=pytz.timezone("Asia/Taipei"))

    pending = db.pending.find_one({"user_id": param.user_id})
    restaurants = pending["pools"]
    while True:
        data_id = "".join(
            random.choice(string.ascii_letters + string.digits) for x in range(10)
        )
        # _id 尚未被使用
        if not db.vote.find_one({"_id": data_id}):
            break
    data = {
        "_id": data_id,
        "restaurants": restaurants,
        "creator": param.user_id,
        "vote_name": param.vote_name,
        "vote_end": param.vote_end,
        "start_date": param.start_date,
        "num_days": param.num_days,
        "min_time": param.min_time,
        "max_time": param.max_time,
        "create_time": now,
        "participants": {},
    }
    db.vote.insert_one(data)
