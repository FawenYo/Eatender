import json
import random
import string
import sys
from collections import Counter
from datetime import datetime
from typing import Optional

import pytz
from bson import json_util
from dateutil import parser
from fastapi import APIRouter, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from .model import *

sys.path.append(".")
import config

vote = APIRouter()
templates = Jinja2Templates(directory="templates")

headers = {"content-type": "application/json; charset=utf-8"}


weekday_text = {
    0: "（一）",
    1: "（二）",
    2: "（三）",
    3: "（四）",
    4: "（五）",
    5: "（六）",
    6: "（日）",
}


@vote.get("/share", response_class=HTMLResponse)
async def share(
    request: Request,
    pull_id: str,
) -> HTMLResponse:
    """分享投票資訊頁面

    Args:
        request (Request): Request Object

    Returns:
        HTMLResponse: 投票資訊頁面
    """
    return templates.TemplateResponse("share.html", context={"request": request})


@vote.get("/login", response_class=HTMLResponse)
async def login(
    request: Request, liff_state: Optional[str] = Query(None, alias="liff.state")
) -> HTMLResponse:
    """轉址至餐廳投票頁面

    Args:
        request (Request): Request Object

    Returns:
        HTMLResponse: 轉址頁面
    """
    return templates.TemplateResponse("login.html", context={"request": request})


@vote.get("/vote/create")
async def vote_create_page(
    request: Request,
    liff_state: Optional[str] = Query(None, alias="liff.state"),
    user_id: Optional[str] = "",
) -> JSONResponse:
    return templates.TemplateResponse("vote_create.html", context={"request": request})


@vote.get("/vote")
async def vote_page(request: Request, id: str, name: str) -> HTMLResponse:
    """餐廳投票頁面

    Args:
        request (Request): Request Object
        id (str): 投票池ID
        name (str): 使用者ID

    Returns:
        HTMLResponse: 餐廳投票頁面
    """
    return templates.TemplateResponse(
        "restaurant.html",
        context={"request": request},
    )


@vote.post("/api/vote/create/event", response_class=JSONResponse)
async def vote_create(param: CreateVote) -> JSONResponse:
    now = datetime.now(tz=pytz.timezone("Asia/Taipei"))

    user_data = config.db.user.find_one({"user_id": param.user_id})
    if user_data:
        restaurants = user_data["vote"]
        if restaurants != []:
            while True:
                data_id = "".join(
                    random.choice(string.ascii_letters + string.digits)
                    for x in range(10)
                )
                # _id 尚未被使用
                if not config.db.vote.find_one({"_id": data_id}):
                    break
            dates = []
            for each in param.date_range:
                for session in param.time_session:
                    date_string = f"{each['year']}/{each['month']}/{each['day']}"
                    date = parser.parse(date_string)
                    week_day = date.weekday()
                    dates.append(f"{date_string} {weekday_text[week_day]} {session}")
            data = {
                "_id": data_id,
                "restaurants": restaurants,
                "creator": param.user_id,
                "vote_name": param.vote_name,
                "due_date": param.due_date,
                "dates": dates,
                "create_time": now,
                "participants": {},
            }
            if param.user_id != "example":
                config.db.vote.insert_one(data)

                user_data["vote"] = []
                config.db.user.update_one()(
                    {"user_id": param.user_id}, {"$set": user_data}
                )
            message = {
                "status": "success",
                "message": {
                    "title": "投票已成功建立！",
                    "content": "前往分享頁面",
                    "share_link": f"{config.SITE_NAME}share?pull_id={data_id}",
                },
            }
        else:
            message = {"status": "failed", "error_message": "投票池內沒有餐廳！"}
    else:
        message = {"status": "failed", "error_message": "查無使用者資料！"}
    return JSONResponse(content=message, headers=headers)


@vote.get("/api/vote/get/restaurant", response_class=JSONResponse)
async def get_pull_data(pull_id: str) -> JSONResponse:
    """取得投票池餐廳資訊

    Args:
        pull_id (str): 投票池ID

    Returns:
        JSONResponse: 餐廳資訊
    """
    pull_data = config.db.vote.find_one({"_id": pull_id})
    if pull_data:
        restaurants = []
        if pull_id != "example":
            for each in pull_data["restaurants"]:
                data = json.loads(config.cache.get(each))
                restaurants.append(data)
        else:
            random_restaurants = config.db.restaurant.aggregate(
                [{"$sample": {"size": 5}}]
            )
            for each in random_restaurants:
                restaurants.append(each)
        message = {"status": "success", "restaurants": restaurants}
    else:
        message = {"status": "error", "error_message": "Vote pull not found."}
    return JSONResponse(content=json.loads(json_util.dumps(message)))


@vote.post("/api/vote/save/restaurant", response_class=JSONResponse)
async def vote_save(param: SaveVoteRestaurant) -> JSONResponse:
    """儲存餐廳投票結果

    Args:
        param (SaveVoteRestaurant): 餐廳投票資訊

    Returns:
        JSONResponse: 儲存結果
    """
    pull_id = param.pull_id
    user_id = param.user_id
    choose_result = param.choose_result

    pull_data = config.db.vote.find_one({"_id": pull_id})
    if pull_data:
        # 曾經投票過
        if user_id in pull_data["participants"]:
            pull_data["participants"][user_id]["restaurants"] = choose_result["love"]
        else:
            pull_data["participants"][user_id] = {
                "restaurants": choose_result["love"],
                "time": [],
            }
        config.db.vote.update_one({"_id": pull_id}, {"$set": pull_data})
        message = {"status": "success", "message": "已成功儲存！"}
    else:
        message = {"status": "error", "error_message": "查無投票！"}
    return JSONResponse(content=message, headers=headers)


@vote.get("/api/vote/get/date", response_class=JSONResponse)
async def vote_date_get(pull_id: str) -> JSONResponse:
    """投票 - 取得投票日期資訊
    Args:
        pull_id (str): 投票池ID
    Returns:
        JSONResponse: 投票日期資訊
    """

    vote_data = config.db.vote.find_one({"_id": pull_id})
    result_data = {"vote_name": "", "dates": []}
    if vote_data:
        result_data["vote_name"] = vote_data["vote_name"]
        result_data["dates"] = vote_data["dates"]

        message = {"status": "success", "data": result_data}
    else:
        message = {"status": "error", "error_message": "找不到投票內容！"}
    return JSONResponse(content=message, headers=headers)


@vote.post("/api/vote/save/date", response_class=JSONResponse)
async def vote_date_save(param: SaveVoteDate) -> JSONResponse:
    """儲存日期投票結果

    Args:
        param (SaveVoteDate): 投票日期資訊

    Returns:
        JSONResponse: 儲存結果
    """
    pull_id = param.pull_id
    user_id = param.user_id
    available_date = param.available_date

    pull_data = config.db.vote.find_one({"_id": pull_id})
    if pull_data:
        pull_data["participants"][user_id]["time"] = available_date
        config.db.vote.update_one({"_id": pull_id}, {"$set": pull_data})
        message = {"status": "success", "message": "已成功儲存投票內容！"}
    else:
        message = {"status": "error", "error_message": "查無投票！"}
    return JSONResponse(content=message, headers=headers)


def get_vote_result(pull_id: str):
    vote_data = config.db.vote.find_one({"_id": pull_id})

    restaurants = vote_data["restaurants"]
    vote_restaurants = []
    vote_time = []

    for user, user_vote in vote_data["participants"].items():
        vote_restaurants += user_vote["restaurants"]
        vote_time += user_vote["time"]

    result_restaurants = []
    for restaurant_index, count in Counter(vote_restaurants).most_common(3):
        result_restaurants.append(restaurants[restaurant_index])
    # TODO: 時間
