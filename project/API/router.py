import sys
from datetime import datetime

from fastapi import APIRouter
from fastapi.responses import JSONResponse

import config
from weather.main import Weather

sys.path.append(".")
from food.main import Nearby_restaurant
from line.templates import Template

api = APIRouter()


# API - 當地天氣
@api.get("/api/weather/")
async def weather(loc: str):
    try:
        lat, lng = loc.split(",")
        weather_data = Weather()
        weather_data.fetch_data(lat=lat, lng=lng)
        config.console.log(weather_data.__dict__)
        return weather_data.__dict__
    except KeyError:
        error_message = {"status": "error", "error_message": "Parameters value error."}
        return error_message


# API - 地點附近餐廳
@api.get("/api/restaurant/")
async def restaurant(keyword: str, loc: str):
    start = datetime.now()
    try:
        latitude, longitude = loc.split(",")
        restaurant_data = Nearby_restaurant(
            latitude=latitude, longitude=longitude, keyword=keyword
        )
        restaurant_data.get_info()
        config.console.log(restaurant_data.__dict__)
        end = datetime.now()
        return f"Total Process Time: {end - start}."
    except KeyError:
        error_message = {"status": "error", "error_message": "Parameters value error."}
        return error_message


# API - LIFF share Flex template
@api.get("/api/liffshare")
async def liff_share(pull_id: str):
    message = Template().liff_share(pull_id=pull_id)
    return {"status": "success", "data": message}


# API - Vote page restaurant data
@api.get("/api/vote/{pull_id}", response_class=JSONResponse)
async def get_pull_data(pull_id):
    pull_data = config.db.vote_pull.find_one({"_id": pull_id})
    if pull_data:
        message = {"status": "success", "restaurants": pull_data["restaurants"]}
    else:
        message = {"status": "error", "error_message": "Vote pull not found."}
    return message
