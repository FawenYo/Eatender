import json
import random
import string
import sys
from datetime import datetime

import pytz
from bson import json_util
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from .model import *

sys.path.append(".")
import config

vote = APIRouter()
templates = Jinja2Templates(directory="templates")

headers = {"content-type": "application/json; charset=utf-8"}


@vote.get("/share", response_class=HTMLResponse)
async def share(request: Request) -> HTMLResponse:
    """分享投票資訊頁面

    Args:
        request (Request): Request Object

    Returns:
        HTMLResponse: 投票資訊頁面
    """
    return templates.TemplateResponse("share.html", context={"request": request})


@vote.get("/login", response_class=HTMLResponse)
async def login(request: Request) -> HTMLResponse:
    """轉址至餐廳投票頁面

    Args:
        request (Request): Request Object

    Returns:
        HTMLResponse: 轉址頁面
    """
    return templates.TemplateResponse("login.html", context={"request": request})


@vote.get("/vote/create")
async def vote_create_page(request: Request, user_id: str) -> JSONResponse:
    message = {"status": "success", "message": "頁面維護中"}
    return JSONResponse(content=message, headers=headers)


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

    pending = config.db.pending.find_one({"user_id": param.user_id})
    restaurants = pending["pools"]
    while True:
        data_id = "".join(
            random.choice(string.ascii_letters + string.digits) for x in range(10)
        )
        # _id 尚未被使用
        if not config.db.vote.find_one({"_id": data_id}):
            break
    data = {
        "_id": data_id,
        "restaurants": restaurants,
        "creator": param.user_id,
        "vote_name": param.vote_name,
        "vote_end": param.vote_end,
        "start_date": param.start_date,
        "num_days": param.num_days,
        "min_time": param.min_time,
        "max_time": param.max_time,
        "create_time": now,
        "participants": {},
    }
    config.db.vote.insert_one(data)
    message = {"status": "success", "message": "已成功建立投票！"}
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
        for each in pull_data["restaurants"]:
            data = json.loads(config.cache.get(each))
            restaurants.append(data)
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
async def vote_date_get(pull_id: str, user_id: str) -> JSONResponse:
    """投票 - 取得投票日期資訊

    Args:
        pull_id (str): 投票池ID

    Returns:
        JSONResponse: 投票日期資訊
    """

    vote_data = config.db.vote.find_one({"_id": pull_id})
    if vote_data:
        del vote_data["_id"]
        del vote_data["restaurants"]
        del vote_data["creator"]
        del vote_data["create_time"]
        vote_data["last_select"] = vote_data["participants"][user_id]["time"]  # 選擇時間紀錄
        del vote_data["participants"]

        message = {"status": "success", "data": vote_data}
    else:
        message = {"status": "failed", "error_message": "找不到投票內容！"}
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
    dates = param.dates

    pull_data = config.db.vote.find_one({"_id": pull_id})
    if pull_data:
        pull_data["participants"][user_id]["time"] = dates
        print("saved")
        config.db.vote.update_one({"_id": pull_id}, {"$set": pull_data})
        message = {"status": "success", "message": "已成功儲存！"}
    else:
        message = {"status": "error", "error_message": "查無投票！"}
    message = {"status": "success"}
    return JSONResponse(content=message, headers=headers)
