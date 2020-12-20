import os
import threading

import pymongo
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()

console = Console()
# LINE Bot 設定
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")

# Google Maps API
GOOGLE_MAPS_APIKEY = os.environ.get("GOOGLE_MAPS_APIKEY")
GOOGLE_MAPS_REQUEST_FIELD = [
    "formatted_address",
    "url",
    "formatted_phone_number",
    "website",
    "opening_hours",
    "price_level",
    "review",
]

# MongoDB
MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PWD = os.environ.get("MONGO_PWD")

client = pymongo.MongoClient(
    f"mongodb+srv://{MONGO_USER}:{MONGO_PWD}@cluster0.db2o0.mongodb.net/db?retryWrites=true&w=majority"
)

db = client.db

# Global vars
restaurants = {}


def init_restaurants():
    db_results = db.restaurants.find({})
    for each in db_results:
        place_id = each["place_id"]
        restaurants[place_id] = each


threading.Thread(target=init_restaurants).start()
