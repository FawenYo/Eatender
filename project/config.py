import json
import os
import threading

import pymongo
import redis
import sentry_sdk
from dotenv import load_dotenv
from lotify.client import Client
from rich.console import Console

# Load environment variables
load_dotenv()

console = Console()
profile = os.getenv("profile", "production")
run_env = os.getenv("run_env", "local")

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
client = pymongo.MongoClient()

db = client.db

# Redis
if run_env == "docker":
    redis_host = "redis"
else:
    redis_host = "127.0.0.1"
cache = redis.Redis(host=redis_host, port=6379)


def init_restaurants():
    db_results = db.restaurant.find({})
    for each in db_results:
        del each["_id"]
        del each["time"]
        place_id = each["place_id"]
        cache.set(place_id, json.dumps(each))


threading.Thread(target=init_restaurants).start()

# Github repo url
GITHUB_REPO_URL = os.environ.get("GITHUB_REPO_URL")
