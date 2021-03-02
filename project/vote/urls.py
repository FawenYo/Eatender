import json
import random
import string
import sys
from datetime import datetime
from typing import Optional

import pytz
from bson import json_util
from dateutil import parser
from fastapi import APIRouter, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from linebot import LineBotApi

from .model import *

sys.path.append(".")
import config

vote = APIRouter()
templates = Jinja2Templates(directory="templates")

headers = {"content-type": "application/json; charset=utf-8"}
line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)


@vote.get("/share", response_class=HTMLResponse)
async def share(
    request: Request,
    pull_id: Optional[str],
    liff_state: Optional[str] = Query(None, alias="liff.state"),
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
    """轉址至投票頁面

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


@vote.get("/view/result", response_class=HTMLResponse)
async def login(
    request: Request, liff_state: Optional[str] = Query(None, alias="liff.state")
) -> HTMLResponse:
    """轉址至投票結果頁面

    Args:
        request (Request): Request Object

    Returns:
        HTMLResponse: 轉址頁面
    """
    return templates.TemplateResponse("liff_result.html", context={"request": request})


@vote.get("/vote/result")
async def vote_result_page(request: Request, pull_id: str) -> HTMLResponse:
    """投票結果頁面

    Args:
        request (Request): Request Object
        pull_id (str): 投票池ID

    Returns:
        HTMLResponse: 投票結果頁面
    """
    return templates.TemplateResponse(
        "vote_result.html",
        context={"request": request},
    )


@vote.post("/api/vote/create/event", response_class=JSONResponse)
async def vote_create(param: CreateVote) -> JSONResponse:
    """創建投票

    Args:
        param (CreateVote): 投票資訊

    Returns:
        JSONResponse: 創建結果
    """
    now = datetime.now(tz=pytz.timezone("Asia/Taipei"))

    user_data = config.db.user.find_one({"user_id": param.user_id})
    if user_data:
        # 餐廳列表
        restaurants = user_data["vote"]
        if restaurants != []:
            # 設定 _id
            while True:
                data_id = "".join(
                    random.choice(string.ascii_letters + string.digits)
                    for x in range(10)
                )
                # _id 尚未被使用
                if not config.db.vote.find_one({"_id": data_id}):
                    break

            # 日期列表
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
                "result": {"user": {}, "restaurants": {}, "dates": {}, "best": {}},
            }
            # 餐廳
            for each_restaurant in restaurants:
                data["result"]["restaurants"][each_restaurant] = 0
            for each_date in dates:
                # 日期
                data["result"]["dates"][each_date] = 0

                # 綜合
                date_string, day_text, session = each_date.split(" ")
                for each_restaurant in restaurants:
                    data["result"]["best"][
                        f"{date_string} {day_text} + {session} @ {each_restaurant}"
                    ] = []

            # 非測試範例
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
        restaurants = []
        for restaurant_id in choose_result["love"]:
            restaurant_place_id = pull_data["restaurants"][restaurant_id]
            restaurants.append(restaurant_place_id)
            pull_data["result"]["restaurants"][restaurant_place_id] += 1

        # 曾經投票過
        if user_id in pull_data["result"]["user"]:
            pull_data["result"]["user"][user_id]["restaurants"] = restaurants
        else:
            pull_data["result"]["user"][user_id] = {
                "restaurants": restaurants,
                "dates": [],
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
        pull_data["result"]["user"][user_id]["dates"] = available_date

        for each_date in available_date:
            # 日期
            pull_data["result"]["dates"][each_date] += 1

            # 綜合
            date_string, day_text, session = each_date.split(" ")
            for each_restaurant in pull_data["result"]["user"][user_id]["restaurants"]:
                pull_data["result"]["best"][
                    f"{date_string} {day_text} + {session} @ {each_restaurant}"
                ].append(user_id)

        config.db.vote.update_one({"_id": pull_id}, {"$set": pull_data})
        message = {"status": "success", "message": "已成功儲存投票內容！"}
    else:
        message = {"status": "error", "error_message": "查無投票！"}
    return JSONResponse(content=message, headers=headers)


@vote.get("/api/vote/get/result", response_class=JSONResponse)
async def api_vote_get_result(pull_id: str) -> JSONResponse:
    """投票 - 取得投票結果

    Args:
        pull_id (str): 投票池ID

    Returns:
        JSONResponse: 投票結果
    """
    vote_data = find_vote_result(pull_id=pull_id)
    result_data = {
        "vote_name": "",
        "best": {},
        "restaurants": {},
        "dates": {},
        "most_best": [],
        "most_restaurants": [],
        "most_dates": [],
    }
    if vote_data:
        result_data["vote_name"] = vote_data["data"]["info"]["vote_name"]
        sorted_best = vote_data["data"]["sorted_best"]
        sorted_restaurants = vote_data["data"]["sorted_restaurants"]
        sorted_dates = vote_data["data"]["sorted_dates"]

        # 綜合
        for count, info in sorted_best:
            # 最多次的綜合
            if result_data["most_best"] == []:
                for each, users in info:
                    info_date, info_rid = each.split(" @ ")
                    info_date = info_date.replace("+ ", "")
                    restaurant = json.loads(config.cache.get(info_rid))
                    result_data["most_best"].append(
                        f"{info_date} @ {restaurant['name']}"
                    )

            for each, users in info:
                info_date, info_rid = each.split(" @ ")
                info_date = info_date.replace("+ ", "")
                restaurant = json.loads(config.cache.get(info_rid))
                result_data["best"][f"{info_date} @ {restaurant['name']}"] = count

        # 餐廳
        for count, restaurants_pid in sorted_restaurants:
            # 最多次的餐廳
            if result_data["most_restaurants"] == []:
                for each in restaurants_pid:
                    restaurant = json.loads(config.cache.get(each))
                    result_data["most_restaurants"].append(restaurant["name"])

            for each in restaurants_pid:
                restaurant = json.loads(config.cache.get(each))
                result_data["restaurants"][restaurant["name"]] = count

        # 日期
        for count, dates in sorted_dates:
            # 最多次的日期
            if result_data["most_dates"] == []:
                result_data["most_dates"] = dates

            for each in dates:
                result_data["dates"][each] = count
        message = {"status": "success", "data": result_data}
    else:
        message = {"status": "error", "error_message": "找不到投票內容！"}
    return JSONResponse(content=message, headers=headers)


def find_vote_result(pull_id: str) -> dict:
    """排序投票結果

    Args:
        pull_id (str): 投票池ID

    Returns:
        dict: 排序結果
    """
    vote_data = config.db.vote.find_one({"_id": pull_id})
    if vote_data:
        restaurants = vote_data["result"]["restaurants"]
        dates = vote_data["result"]["dates"]
        best = vote_data["result"]["best"]

        # 餐廳
        reverse_restaurants = {}
        for restaurant_id, count in restaurants.items():
            if count in reverse_restaurants:
                reverse_restaurants[count].append(restaurant_id)
            else:
                reverse_restaurants[count] = [restaurant_id]
        sorted_restaurants = sorted(reverse_restaurants.items(), key=lambda x: -x[0])

        # 時間
        reverse_dates = {}
        for each_date, count in dates.items():
            if count in reverse_dates:
                reverse_dates[count].append(each_date)
            else:
                reverse_dates[count] = [each_date]
        sorted_dates = sorted(reverse_dates.items(), key=lambda x: -x[0])

        # 綜合
        reverse_best = {}
        for each_choose, users in best.items():
            count = len(users)
            if count in reverse_best:
                reverse_best[count].append((each_choose, users))
            else:
                reverse_best[count] = [(each_choose, users)]
        sorted_best = sorted(reverse_best.items(), key=lambda x: -x[0])

        data = {
            "status": "success",
            "data": {
                "info": vote_data,
                "sorted_best": sorted_best,
                "sorted_restaurants": sorted_restaurants,
                "sorted_dates": sorted_dates,
            },
        }
    else:
        data = {"status": "error", "error_message": "找不到投票內容！"}
    return data


def show_result(pull_id: str) -> dict:
    """LINE投票結果

    Args:
        pull_id (str): 投票池ID

    Returns:
        dict: 投票結果
    """
    result = find_vote_result(pull_id=pull_id)
    vote_name = result["data"]["info"]["vote_name"]
    count, best_info = result["data"]["sorted_best"][0]
    best = []
    users = []
    for date_info, user_info in best_info:
        info_date, info_rid = date_info.split(" @ ")
        info_date = info_date.replace("+ ", "")
        restaurant = json.loads(config.cache.get(info_rid))

        best.append(f"{info_date} @ {restaurant['name']}")
        for each_user_id in user_info:
            try:
                user_name = line_bot_api.get_profile(each_user_id).display_name
            except:
                user_name = each_user_id

            if user_name not in users:
                users.append(user_name)
    return {"vote_name": vote_name, "best": best, "users": users}
