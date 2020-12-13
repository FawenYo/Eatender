import sys
import threading

from flask import Blueprint, abort, current_app, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

from weather.main import Weather

# 上層目錄import
sys.path.append(".")
import config
import MongoDB.operation as database
from food.main import Restaurant_data
from line.templates import Template

line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.LINE_CHANNEL_SECRET)

line_app = Blueprint("line_app", __name__)


@line_app.route("/callback", methods=["POST"])
def callback():
    """LINE Server Webhook Callback

    Raises:
        HTML status code 400: InvalidSignatureError
    Returns:
        str: "OK"
    """
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    current_app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


@handler.add(FollowEvent)
def handle_follow(event):
    """事件 - 新使用者加入Bot

    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#follow-event
    """
    reply_token = event.reply_token
    message = TextSendMessage(text="那你真的很懂吃ㄟ🈹️")
    line_bot_api.reply_message(reply_token, message)
    database.new_user(user_id=event.source.user_id)


@handler.add(UnfollowEvent)
def handle_unfollow(event):
    """事件 - 新使用者封鎖Bot

    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#unfollow-event
    """
    database.delete_user(user_id=event.source.user_id)


@handler.add(MessageEvent, message=(TextMessage, LocationMessage))
def handle_message(event):
    """事件 - 訊息

    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#message-event
    """
    user_id = event.source.user_id
    reply_token = event.reply_token
    if isinstance(event.message, TextMessage):
        user_message = event.message.text
        # 測試階段，直接回覆使用者輸入內容
        message = TextSendMessage(text=user_message)
        line_bot_api.reply_message(reply_token, message)
    elif isinstance(event.message, LocationMessage):
        lat = event.message.latitude
        lng = event.message.longitude
        # 記錄使用者位置
        thread = threading.Thread(
            target=database.record_user_location, args=(user_id, lat, lng)
        )
        thread.start()
        # TODO: 讓使用者能自己設定餐廳類別
        keyword = "餐廳"
        restaurants = Restaurant_data(latitude=lat, longitude=lng)
        restaurants.get_info()
        # Show first five restaurant
        message = Template().show_nearby_restaurant(
            restaurants=restaurants.restaurants[:5]
        )
        line_bot_api.reply_message(reply_token, message)
