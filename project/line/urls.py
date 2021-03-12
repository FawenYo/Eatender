import sys
from typing import Optional

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from munch import munchify

from . import flex_template, message_event, postback_event, user_event

sys.path.append(".")

import config
from vote.urls import show_result

line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.LINE_CHANNEL_SECRET)

line_app = APIRouter()
templates = Jinja2Templates(directory="templates")


@line_app.get("/notify/", response_class=RedirectResponse)
async def line_notify_redirect(uid: Optional[str] = "") -> RedirectResponse:
    """轉址至 LINE Notify 綁定頁面

    Args:
        uid (Optional[str], optional): 使用者 LINE ID. Defaults to "".

    Returns:
        RedirectResponse: LINE Notify 綁定頁面
    """
    link = config.lotify_client.get_auth_link(state=uid)
    return RedirectResponse(link)


@line_app.get("/notify/callback", response_class=HTMLResponse)
async def line_notify_callback(request: Request, code: str = "", state: str = ""):
    """LINE Notify 綁定完成

    Args:
        request (Request): Request Object.
        code (str, optional): LINE Notify access token. Defaults to "".
        state (str, optional): 使用者LINE ID. Defaults to "".

    Returns:
        [type]: [description]
    """
    line_notify_key = config.lotify_client.get_access_token(code=code)

    # 更新資料庫
    result = config.db.user.find_one({"user_id": state})
    result["notify"]["status"] = True
    result["notify"]["token"] = line_notify_key
    config.db.user.update_one({"user_id": state}, {"$set": result})

    return templates.TemplateResponse("bound_notify.html", context={"request": request})


@line_app.post("/callback")
async def callback(request: Request) -> str:
    """LINE Bot Webhook Callback

    Args:
        request (Request): Request Object.

    Raises:
        HTTPException: Signature 驗證失敗

    Returns:
        str: OK
    """
    signature = request.headers["X-Line-Signature"]
    body = await request.body()
    # handle webhook body
    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Missing Parameter")
    return "OK"


@handler.add(FollowEvent)
def handle_follow(event):
    """事件 - 新使用者加入Bot

    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#follow-event
    """
    user_event.handle_follow(event=event)


@handler.add(UnfollowEvent)
def handle_unfollow(event):
    """事件 - 新使用者封鎖Bot

    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#unfollow-event
    """
    user_event.handle_unfollow(event=event)


@handler.add(JoinEvent)
def handle_join(event):
    """事件 - 加入群組/房間

    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#join-event
    """
    user_event.handle_join(event=event)


@handler.add(LeaveEvent)
def handle_leave(event):
    """事件 - 離開群組/房間

    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#leave-event
    """
    user_event.handle_leave(event=event)


@handler.add(MessageEvent, message=(TextMessage, LocationMessage))
def handle_message(event):
    """事件 - 訊息

    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#message-event
    """
    message_event.handle_message(event=event)


@handler.add(PostbackEvent)
def handle_postback(event):
    """事件 - Postback

    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#postback-event
    """
    postback_event.handle_postback(event=event)


@line_app.get("/api/liffshare")
async def liff_share(pull_id: str, target: str) -> JSONResponse:
    """API - 分享投票

    Args:
        pull_id (str): 投票池ID

    Returns:
        JSONResponse: Flex Message資料
    """
    if target == "vote":
        message = [
            {
                "type": "flex",
                "altText": "一起來吃飯吧！",
                "contents": flex_template.share_vote(pull_id=pull_id),
            }
        ]
    else:
        vote_info = show_result(pull_id=pull_id)

        vote_name = vote_info["vote_name"]
        best = vote_info["best"]
        users = vote_info["users"]
        total_user_count = vote_info["total_user_count"]

        restaurants = []
        for each in best:
            i = munchify(each)
            if i.restaurant not in restaurants:
                restaurants.append(i.restaurant)
        message = [
            {
                "type": "flex",
                "altText": "一起來吃飯吧！",
                "contents": flex_template.share_result(
                    pull_id=pull_id,
                    vote_name=vote_name,
                    best=best,
                    users=users,
                    total_user_count=total_user_count,
                ),
            },
            {
                "type": "flex",
                "altText": "餐廳資訊",
                "contents": flex_template.show_restaurant(
                    restaurants=restaurants, web=True
                ),
            },
        ]

    return JSONResponse(
        content={
            "status": "success",
            "data": message,
        }
    )
