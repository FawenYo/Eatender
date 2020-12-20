import sys
from datetime import datetime

from flask import Blueprint, request

from config import console
from weather.main import Weather

# 上層目錄import
sys.path.append(".")
import config
from food.main import Nearby_restaurant

api = Blueprint("api", __name__)


@api.route("/weather/")
def weather():
    try:
        lat, lng = request.args.get("loc").split(",")
        weather_data = Weather()
        weather_data.fetch_data(lat=lat, lng=lng)
        console.log(weather_data.__dict__)
        return weather_data.__dict__
    except KeyError:
        error_message = {"status": "error", "error_message": "Parameters value error."}
        return error_message


@api.route("/restaurant/")
def restaurant():
    start = datetime.now()
    try:
        keyword = request.args.get("keyword")
        latitude, longitude = request.args.get("loc").split(",")
        restaurant_data = Nearby_restaurant(
            latitude=latitude, longitude=longitude, keyword=keyword
        )
        restaurant_data.get_info()
        console.log(restaurant_data.__dict__)
        end = datetime.now()
        return f"Total Process Time: {end - start}."
    except KeyError:
        error_message = {"status": "error", "error_message": "Parameters value error."}
        return error_message
