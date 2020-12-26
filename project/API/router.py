import sys
from datetime import datetime

from config import console
from fastapi import APIRouter, HTTPException, Request
from weather.main import Weather

# 上層目錄import
sys.path.append(".")
import config
from food.main import Nearby_restaurant
from line.templates import Template

api = APIRouter()


@api.get("/api/weather/")
async def weather(loc: str):
    try:
        lat, lng = loc.split(",")
        weather_data = Weather()
        weather_data.fetch_data(lat=lat, lng=lng)
        console.log(weather_data.__dict__)
        return weather_data.__dict__
    except KeyError:
        error_message = {"status": "error", "error_message": "Parameters value error."}
        return error_message


@api.get("/api/restaurant/")
async def restaurant(keyword: str, loc: str):
    start = datetime.now()
    try:
        latitude, longitude = loc.split(",")
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


@api.get("/api/liffshare")
async def liff_share(pull_id: str):
    message = Template().liff_share(pull_id=pull_id)
    return {"status": "success", "data": message}
