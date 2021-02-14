import json
import sys

from bson import json_util
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

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


@vote.get("/api/vote/{pull_id}", response_class=JSONResponse)
async def get_pull_data(pull_id: str) -> JSONResponse:
    """取得投票池餐廳資訊

    Args:
        pull_id (str): 投票池ID

    Returns:
        JSONResponse: 餐廳資訊
    """
    pull_data = config.db.vote_pull.find_one({"_id": pull_id})
    if pull_data:
        message = {"status": "success", "restaurants": pull_data["restaurants"]}
    else:
        message = {"status": "error", "error_message": "Vote pull not found."}
    return JSONResponse(content=json.loads(json_util.dumps(message)))


@vote.post("/api/save/restaurants", response_class=JSONResponse)
async def vote_save(body: dict) -> JSONResponse:
    """儲存餐廳投票結果

    Args:
        body (dict): {"pull_id": 投票池ID (str), "user_id": 使用者ID (str), "choose_result": {"love": [喜歡餐廳index (int), ...], "hate": [討厭餐廳index (int), ...]}}

    Returns:
        JSONResponse: [description]
    """
    pull_id = body["pull_id"]
    user_id = body["user_id"]
    choose_result = body["choose_result"]
    pull_data = config.db.vote_pull.find_one({"_id": pull_id})
    if pull_data:
        pull_data["participants"][user_id] = choose_result["love"]
        config.db.vote_pull.update_one({"_id": pull_id}, {"$set": pull_data})
        message = {"status": "success", "vote_link": pull_data["vote_link"]}
    else:
        message = {"status": "error", "error_message": "查無投票！"}
    return JSONResponse(content=message, headers=headers)


@vote.post("/api/vote/save/date", response_class=JSONResponse)
async def vote_date_save(body: dict) -> JSONResponse:
    """儲存日期投票結果

    Args:
        body (dict): {"user_id": 使用者ID (str), "dates": [日期, ...] (array)}

    Returns:
        JSONResponse: 紀錄成功訊息
    """
    pull_id = body["pull_id"]
    user_id = body["user_id"]
    dates = body["dates"]
    message = {"status": "success"}
    return JSONResponse(content=message, headers=headers)
