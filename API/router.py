import sys

from flask import Blueprint, abort, current_app, request
from flasgger import swag_from
from weather.main import Weather
from config import console

# 上層目錄import
sys.path.append(".")
import config
from food.google_maps.main import GM_Restaurant

api = Blueprint("api", __name__)


@api.route("/weather/?loc=<lat>,<lng>")
@swag_from("../docs/weather_data.yml")
def weather(lat, lng):
    try:
        weather_data = Weather()
        weather_data.fetch_data(lat=lat, lng=lng)
        console.log(weather_data.__dict__)
        return weather_data.__dict__
    except KeyError:
        error_message = {"status": "error", "error_message": "Parameters value error."}
        return error_message


@api.route("/restaurant/")
@swag_from("../docs/restaurant_data.yml")
def restaurant():
    try:
        keyword = request.args.get("keyword")
        latitude, longitude = request.args.get("loc").split(",")
        restaurant_data = GM_Restaurant()
        # FIXME: 還沒parse，目前是直接返回結果
        result = restaurant_data.fetch_data(
            latitude=latitude, longitude=longitude, keyword=keyword
        )
        console.log(result.__dict__)
        return result.__dict__
    except KeyError:
        error_message = {"status": "error", "error_message": "Parameters value error."}
        return error_message
