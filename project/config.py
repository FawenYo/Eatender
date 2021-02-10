import os
import threading

import pymongo
import sentry_sdk
from dotenv import load_dotenv
from lotify.client import Client
from rich.console import Console

# Load environment variables
load_dotenv()

console = Console()
profile = os.getenv("profile", "production")
sentry_sdk.init(os.environ.get("SENTRY_SDK"), traces_sample_rate=1.0)

SITE_NAME = os.environ.get("SITE_NAME")
# LINE Bot 設定
if profile == "local":
    LINE_CHANNEL_SECRET = os.environ.get("TEST_LINE_CHANNEL_SECRET")
    LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("TEST_LINE_CHANNEL_ACCESS_TOKEN")
else:
    LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")
    LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")

# LINE Notify 設定
LINE_NOTIFY_CLIENT_ID = os.environ.get("LINE_NOTIFY_CLIENT_ID")
LINE_NOTIFY_CLIENT_SECRET = os.environ.get("LINE_NOTIFY_CLIENT_SECRET")
LINE_NOTIFY_REDIRECT_URL = os.environ.get("LINE_NOTIFY_REDIRECT_URL")
lotify_client = Client(
    client_id=LINE_NOTIFY_CLIENT_ID,
    client_secret=LINE_NOTIFY_CLIENT_SECRET,
    redirect_uri=LINE_NOTIFY_REDIRECT_URL,
)
AUTHORS_NOTIFY_TOKEN = os.environ.get("AUTHORS_NOTIFY_TOKEN").split(" ")

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

# Github repo url
GITHUB_REPO_URL = os.environ.get("GITHUB_REPO_URL")

# Global vars
restaurants = {}


def init_restaurants():
    db_results = db.restaurants.find({})
    for each in db_results:
        place_id = each["place_id"]
        restaurants[place_id] = each


threading.Thread(target=init_restaurants).start()
