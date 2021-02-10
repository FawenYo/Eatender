import sys
import threading
from datetime import datetime

import sentry_sdk
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from linebot.models import *

from .templates import Template

sys.path.append(".")

import config
import MongoDB.operation as database
from food.main import RestaurantInfo

line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)


def handle_postback(event):
    """事件 - Postback

    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#postback-event
    """
    user_id = event.source.user_id
    reply_token = event.reply_token
    postback_data = event.postback.data
    try:
        if "_||_" in postback_data:
            postback_args = postback_data.split("_||_")
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
                # 尚未收藏餐廳
                if restaurant_data not in user["favorite"]:
                    # 更新收藏列表
                    user["favorite"].append(restaurant_data)
                    config.db.user.update_one({"user_id": user_id}, {"$set": user})

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
                        user_id=user_id,
                        latitude=latitude,
                        longitude=longitude,
                        keyword=keyword,
                    )
                try:
                    line_bot_api.reply_message(reply_token, message)
                # 搜尋超時
                except LineBotApiError as e:
                    sentry_sdk.capture_exception(e)
                    config.console.print_exception()
                    line_bot_api.push_message(user_id, message)
            # 搜尋更多
            elif action == "more":
                latitude, longitude = [float(i) for i in postback_args[1].split(",")]
                keyword = postback_args[2]
                token = postback_args[3]
                token_table = config.db.page_token.find_one({})
                page_token = token_table["data"][token]
                message = find_nearby(
                    user_id=user_id,
                    latitude=latitude,
                    longitude=longitude,
                    keyword=keyword,
                    page_token=page_token,
                )
                try:
                    line_bot_api.reply_message(reply_token, message)
                # 搜尋超時
                except LineBotApiError as e:
                    sentry_sdk.capture_exception(e)
                    config.console.print_exception()
                    # 使用push回應內容
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
                if restaurant_data not in user["vote"]:
                    user["vote"].append(restaurant_data)
                    config.db.user.update_one({"user_id": user_id}, {"$set": user})
                    message = TextSendMessage(text=f"已將{restaurant_data['name']}加入投票池！")
                else:
                    message = TextSendMessage(text=f"餐廳已經在投票池內囉！")
                line_bot_api.reply_message(reply_token, message)
            # 移除投票
            elif action == "remove":
                place_id = postback_args[1]
                user = config.db.user.find_one({"user_id": user_id})
                restaurant_data = config.db.restaurant.find_one({"place_id": place_id})
                if restaurant_data in user["vote"]:
                    user["vote"].remove(restaurant_data)
                    config.db.user.update_one({"user_id": user_id}, {"$set": user})
                    message = TextSendMessage(text=f"已將{restaurant_data['name']}移除投票池！")
                else:
                    message = TextSendMessage(text=f"餐廳不在投票池內！")
                try:
                    line_bot_api.reply_message(reply_token, message)
                # 搜尋超時
                except LineBotApiError as e:
                    sentry_sdk.capture_exception(e)
                    config.console.print_exception()
                    line_bot_api.push_message(user_id, message)
        else:
            # 創建投票
            if postback_data == "create":
                message = TextSendMessage(
                    text=f"請設定投票截止日期",
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                action=DatetimePickerAction(
                                    label="截止日期",
                                    data="endDate",
                                    mode="datetime",
                                )
                            ),
                        ]
                    ),
                )
            # 投票截止日期
            elif postback_data == "endDate":
                vote_pull = config.db.user.find_one({"user_id": user_id})["vote"]
                end_date = datetime.strptime(
                    event.postback.params["datetime"], "%Y-%m-%dT%H:%M"
                )
                data = {
                    "action": "create_event",
                    "user_id": user_id,
                    "end_date": end_date,
                    "pools": vote_pull,
                }
                config.db.pending.insert_one(data)
                message = TextSendMessage(
                    text=f"請依據以下格式輸入投票資訊：\n'投票名稱/投票聚餐日期(西元年-月-日, 多個日期之間以 '|' 連結)/聚餐最早開始時間(小時, 24小時制)/聚餐最晚開始時間(小時, 24小時制)'\n(例如：聖誕聚餐/2020-12-24/18/20)"
                )
            else:
                message = TextSendMessage(text=f"我不知道你在幹嘛QwQ")
            line_bot_api.reply_message(reply_token, message)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        config.console.print_exception()
        message = Template().error()
        line_bot_api.reply_message(reply_token, message)


def find_nearby(
    user_id: str, latitude: float, longitude: float, keyword: str, page_token: str = ""
):
    """搜尋附近餐廳

    Args:
        latitude (float): Location latitude
        longitude (float): Location longitude
        keyword (str): Restaurant name / category
        page_token (str, optional): Google Maps API page token. Defaults to "".
    """
    if keyword == "隨便":
        keyword = ""
    restaurants = RestaurantInfo(
        latitude=latitude, longitude=longitude, keyword=keyword, page_token=page_token
    )
    restaurants.nearby()
    if len(restaurants.restaurants) == 0:
        message = TextSendMessage(text=f"很抱歉，我們找不到相關的餐廳😭")
    else:
        # Show first five restaurant
        message = Template(user_lat=latitude, user_lng=longitude).show_restaurant(
            restaurants=restaurants.restaurants[:5],
            keyword=keyword,
            next_page=restaurants.next_page,
        )
    # 記錄使用者位置
    thread = threading.Thread(
        target=database.record_user_search, args=(user_id, latitude, longitude, keyword)
    )
    thread.start()
    return message
