import sys
import threading

from flask import Blueprint, abort, current_app, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

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
        try:
            pending = config.db.pending.find_one({"user_id": user_id})
            if pending:
                config.db.pending.delete_one({"user_id": user_id})
                latitude = pending["latitude"]
                longitude = pending["longitude"]
                message = find_nearby(
                    latitude=latitude, longitude=longitude, keyword=user_message
                )
            else:
                if user_message == "我的最愛":
                    user_data = config.db.user.find_one({"user_id": user_id})
                    if len(user_data["favorite"]) > 0:
                        message = Template().show_favorite(
                            restaurants=user_data["favorite"][:10]
                        )
                    else:
                        message = TextSendMessage(text="您的最愛列表內還沒有餐廳喔！")
                elif user_message == "投票":
                    user_data = config.db.user.find_one({"user_id": user_id})
                    if len(user_data["vote"]) > 0:
                        message = Template().show_favorite(
                            restaurants=user_data["vote"][:10]
                        )
                    else:
                        message = TextSendMessage(text="您的投票池內還沒有餐廳喔！")
                else:
                    message = TextSendMessage(text="不好意思，我聽不懂你在說什麼呢QwQ")
        except Exception as error:
            message = TextSendMessage(text=f"發生錯誤！\n{error}")
        line_bot_api.reply_message(reply_token, message)
    elif isinstance(event.message, LocationMessage):
        try:
            lat = event.message.latitude
            lng = event.message.longitude
            # 記錄使用者位置
            thread = threading.Thread(
                target=database.record_user_location, args=(user_id, lat, lng)
            )
            thread.start()

            restaurant_category = ["隨便", "日式", "中式", "西式", "咖哩", "其他"]
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
        except Exception as error:
            message = TextSendMessage(text=f"發生錯誤！\n{error}")
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
    try:
        if "_" in postback_data:
            postback_args = postback_data.split("_")
            action = postback_args[0]
            # 加入收藏名單
            if action == "favorite":
                restaurant_id = postback_args[1]
                restaurant_data = config.db.restaurant.find_one(
                    {"place_id": restaurant_id}
                )
                if not restaurant_data:
                    restaurant_data = config.restaurants[restaurant_id]
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
            # 搜尋餐廳
            elif action == "search":
                latitude, longitude = [float(i) for i in postback_args[1].split(",")]
                keyword = postback_args[2]
                if keyword == "其他":
                    data = {
                        "user_id": user_id,
                        "latitude": latitude,
                        "longitude": longitude,
                    }
                    config.db.pending.insert_one(data)
                    message = TextSendMessage(text=f"請輸入餐廳類別或名稱")
                else:
                    message = find_nearby(
                        latitude=latitude, longitude=longitude, keyword=keyword
                    )
                try:
                    line_bot_api.reply_message(reply_token, message)
                # 搜尋超時
                except LineBotApiError:
                    line_bot_api.push_message(user_id, message)
            # 加入投票池
            elif action == "vote":
                restaurant_id = postback_args[1]
                user = config.db.user.find_one({"user_id": user_id})
                restaurant_data = config.db.restaurant.find_one(
                    {"place_id": restaurant_id}
                )
                if not restaurant_data:
                    restaurant_data = config.restaurants[restaurant_id]
                if restaurant_id not in user["vote"]:
                    user["vote"].append(restaurant_data)
                    config.db.user.update_one({"user_id": user_id}, {"$set": user})
                    message = TextSendMessage(text=f"已將{restaurant_data['name']}加入投票池！")
                else:
                    message = TextSendMessage(text=f"餐廳已經在投票池內囉！")
                line_bot_api.reply_message(reply_token, message)
    except Exception as error:
        message = TextSendMessage(text=f"發生錯誤！\n{error}")
        line_bot_api.reply_message(reply_token, message)


def find_nearby(
    latitude,
    longitude,
    keyword,
):
    if keyword == "隨便":
        keyword = ""
    restaurants = Nearby_restaurant(
        latitude=latitude, longitude=longitude, keyword=keyword
    )
    if len(restaurants.restaurants) == 0:
        message = TextSendMessage(text=f"很抱歉，我們找不到相關的餐廳😭")
    else:
        # Show first five restaurant
        message = Template().show_restaurant(restaurants=restaurants.restaurants[:5])
    return message
