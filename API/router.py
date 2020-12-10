import sys

from flasgger import swag_from
from flask import Blueprint, abort, current_app, request

from config import console
from weather.main import Weather

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
