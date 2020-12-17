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
from food.main import Nearby_restaurant
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

        if user_message == "我的最愛":
            user_data = config.db.user.find_one({"user_id": user_id})
            if len(user_data["favorite"]) > 0:
                message = Template().show_favorite(
                    restaurants=user_data["favorite"][:10]
                )
            else:
                message = TextSendMessage(text="您的最愛列表內還沒有餐廳喔！")
        else:
            message = TextSendMessage(text="不好意思，我聽不懂你在說什麼呢QwQ")
        line_bot_api.reply_message(reply_token, message)
    elif isinstance(event.message, LocationMessage):
        lat = event.message.latitude
        lng = event.message.longitude
        # 記錄使用者位置
        thread = threading.Thread(
            target=database.record_user_location, args=(user_id, lat, lng)
        )
        thread.start()

        restaurant_category = ["隨便", "日式", "中式", "西式", "咖哩"]
        quick_reply_items = [
            QuickReplyButton(
                action=PostbackAction(
                    label=category,
                    display_text=category,
                    data=f"search_{lat},{lng}_{category}",
                )
            )
            for category in restaurant_category
        ]

        message = TextSendMessage(
            text="請選擇餐廳類別",
            quick_reply=QuickReply(items=quick_reply_items),
        )
        line_bot_api.reply_message(reply_token, message)


@handler.add(PostbackEvent)
def handle_postback(event):
    """事件 - Postback

    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#postback-event
    """
    user_id = event.source.user_id
    reply_token = event.reply_token
    postback_data = event.postback.data

    if "_" in postback_data:
        postback_args = postback_data.split("_")
        action = postback_args[0]
        if action == "favorite":
            restaurant_id = postback_data[1]
            restaurant_data = config.db.restaurant.find_one({"place_id": restaurant_id})
            user = config.db.user.find_one({"user_id": user_id})
            if restaurant_data not in user["favorite"]:
                # update user favorite list
                user["favorite"].append(restaurant_data)
                config.db.user.update_one({"user_id": user_id}, {"$set": user})
                # reply message
                message = TextSendMessage(text=f"已將{restaurant_data['name']}加入最愛！")
            else:
                message = TextSendMessage(text=f"已經有like過相同的餐廳囉！")
            line_bot_api.reply_message(reply_token, message)
        elif action == "search":
            latitude, longitude = [float(i) for i in postback_args[1].split(",")]
            keyword = postback_args[2]
            if keyword == "隨便":
                keyword = ""
            restaurants = Nearby_restaurant(
                latitude=latitude, longitude=longitude, keyword=keyword
            )
            # Show first five restaurant
            message = Template().show_restaurant(
                restaurants=restaurants.restaurants[:5]
            )
            line_bot_api.reply_message(reply_token, message)
