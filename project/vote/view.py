import sys

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

# 上層目錄import
sys.path.append(".")
import config

vote = APIRouter()
templates = Jinja2Templates(directory="templates")

headers = {"content-type": "application/json; charset=utf-8"}


@vote.get("/share", response_class=HTMLResponse)
async def share(request: Request):
    return templates.TemplateResponse("share.html", context={"request": request})


@vote.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", context={"request": request})


@vote.get("/vote")
async def vote_page(request: Request, id: str, name: str):
    message = await get_pull_data(pull_id=id)
    if message["status"] == "success":
        return templates.TemplateResponse(
            "restaurant.html",
            context={
                "request": request,
                "data": message["restaurants"],
                "name": name,
                "pull_id": id,
            },
        )
    else:
        return message


# 取得投票餐廳
@vote.post("/api/vote/{pull_id}", response_class=JSONResponse)
async def get_pull_data(pull_id):
    pull_data = config.db.vote_pull.find_one({"_id": pull_id})
    if pull_data:
        message = {"status": "success", "restaurants": pull_data["restaurants"]}
    else:
        message = {"status": "error", "error_message": "Vote pull not found."}
    return message


# 紀錄餐廳投票結果
@vote.post("/api/save/restaurants", response_class=JSONResponse)
async def vote_save(body: dict):
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
