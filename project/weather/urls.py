import sys

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from .main import Weather

sys.path.append(".")
import config

weather = APIRouter()


@weather.get("/api/weather/", response_class=JSONResponse)
async def get_weahter(loc: str) -> JSONResponse:
    """當地天氣資料

    Args:
        loc (str): 地點座標(緯度,經度)

    Returns:
        JSONResponse: 當地天氣資料
    """
    try:
        lat, lng = loc.split(",")
        weather_data = Weather()
        weather_data.fetch_data(latitude=lat, longitude=lng)
        config.console.log(weather_data.__dict__)
        return JSONResponse(content=weather_data.__dict__)
    except KeyError:
        error_message = {"status": "error", "error_message": "Parameters value error."}
        return JSONResponse(content=error_message)
