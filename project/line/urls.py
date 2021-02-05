import sys

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

sys.path.append(".")
from typing import Optional

import config
from line import message_event, postback_event, user_event

line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.LINE_CHANNEL_SECRET)

line_app = APIRouter()

# LINE Notify Redirect
@line_app.get("/notify/", response_class=RedirectResponse)
async def line_notify_redirect(uid: Optional[str] = ""):
    # 轉址至綁定 LINE Notify 頁面
    link = config.lotify_client.get_auth_link(state=uid)
    return RedirectResponse(link)


# Line Notify Callback
@line_app.get("/notify/callback", response_class=RedirectResponse)
async def line_notify_callback(code: str = "", state: str = ""):
    line_notify_key = config.lotify_client.get_access_token(code=code)

    # 更新資料庫
    result = config.db.user.find_one({"user_id": state})
    result["notify"]["status"] = True
    result["notify"]["token"] = line_notify_key
    config.db.user.update_one({"user_id": state}, {"$set": result})

    # TODO: 綁定成功提示
    return RedirectResponse(config.SITE_NAME)


# LINE Bot Webhook callback
@line_app.post("/callback")
async def callback(request: Request):
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
