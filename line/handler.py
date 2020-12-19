import sys
import threading
from datetime import datetime

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
from vote.main import create_event

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
                if pending["action"] == "search":
                    config.db.pending.delete_one({"user_id": user_id})
                    latitude = pending["latitude"]
                    longitude = pending["longitude"]
                    message = find_nearby(
                        latitude=latitude, longitude=longitude, keyword=user_message
                    )
                else:
                    (
                        status,
                        event_name,
                        available_dates,
                        no_earlier,
                        no_later,
                    ) = parse_string(message=user_message)
                    pass
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
                        message = [
                            Template().show_favorite(
                                restaurants=user_data["vote"][:10]
                            ),
                            TextSendMessage(
                                text="請確認投票名單是否正確",
                                quick_reply=QuickReply(
                                    items=[
                                        QuickReplyButton(
                                            action=PostbackAction(
                                                label="創建",
                                                data=f"create",
                                            )
                                        )
                                    ]
                                ),
                            ),
                        ]
                    else:
                        message = TextSendMessage(text="您的投票池內還沒有餐廳喔！")
                else:
                    message = TextSendMessage(text="不好意思，我聽不懂你在說什麼呢QwQ")
        except Exception as error:
            config.console.print_exception()
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
                        "action": "search",
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
        else:
            if postback_data == "create":
                message = TextSendMessage(
                    text=f"請設定投票截止日期",
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                action=DatetimePickerAction(
                                    label="截止日期",
                                    data="endDate",
                                    mode="date",
                                )
                            ),
                        ]
                    ),
                )
            elif postback_data == "endDate":
                vote_pull = config.db.user.find_one({"user_id": user_id})["vote"]
                end_date = event.postback.params["date"]
                data = {
                    "action": "create_event",
                    "user_id": user_id,
                    "end_date": end_date,
                    "pools": vote_pull,
                }
                config.db.pending.insert_one(data)
                message = TextSendMessage(
                    text=f"請依據 '投票名稱/投票日期(%Y-%m-%d, 多日期之間以 '|' 連結)/最早時間(小時, 24小時制)/最晚時間(小時, 24小時制)' 格式輸入投票資訊"
                )
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


def parse_string(message):
    # default
    status = False
    event_name = ""
    available_dates = ""
    no_earlier = 0
    no_later = 24

    if not message:
        # input是空字串，回傳預設值
        return status, event_name, available_dates, no_earlier, no_later

    temp = message.split("/")
    date_candidates = ""
    daytime_constraint = []
    for each in temp:
        if "-" in each:
            date_candidates = each
        elif each.isdigit():
            daytime_constraint.append(int(each))
        else:
            event_name = each

    if not date_candidates:
        # 沒有輸入日期
        pass
    else:
        correct_date = None
        dates = date_candidates.split("|")
        for date in dates:
            try:
                new_date = datetime.strptime(date, "%Y-%m-%d")
                correct_date = True
            except ValueError:
                correct_date = False
    if correct_date:
        available_dates = date_candidates
    else:
        # 日期輸入格式錯誤
        pass

    if not daytime_constraint:
        # 沒有輸入時間限制
        pass
    else:
        no_earlier = min(daytime_constraint)
        no_later = max(daytime_constraint)
        if (no_earlier < 0 or 
                no_later > 24 or
                no_earlier == no_later):
            # 時間限制格式錯誤
            pass

    if not event_name:
        # 沒有輸入事件名稱
        pass

    return status, event_name, available_dates, no_earlier, no_later
