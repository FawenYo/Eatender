import sys
import threading

import requests
import sentry_sdk
from bs4 import BeautifulSoup
from linebot import LineBotApi
from linebot.models import *

from . import flex_template

sys.path.append(".")

import config
import MongoDB.operation as database
from food.main import RestaurantInfo
from vote.urls import show_result
from weather.main import Weather

line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)


def handle_message(event):
    """事件 - 訊息

    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#message-event
    """
    can_reply = True
    user_id = event.source.user_id
    reply_token = event.reply_token

    # 文字訊息
    if isinstance(event.message, TextMessage):
        user_message = event.message.text
        user_message = user_message.replace("＠", "@")
        try:
            pending = config.db.pending.find_one({"user_id": user_id})
            # QA問答
            if pending:
                # 取消操作
                if user_message == "取消":
                    config.db.pending.delete_one({"user_id": user_id})
                    message = TextSendMessage(text=f"已取消操作！")
                else:
                    # 餐廳關鍵字
                    config.db.pending.delete_one({"user_id": user_id})
                    latitude = pending["latitude"]
                    longitude = pending["longitude"]
                    message = find_nearby(
                        user_id=user_id,
                        latitude=latitude,
                        longitude=longitude,
                        keyword=user_message,
                    )

            # 文字訊息
            else:
                # 教學
                if user_message == "教學":
                    message = flex_template.tutorial()
                    line_bot_api.reply_message(reply_token, message)

                # 我的最愛
                if user_message == "我的最愛":
                    user_data = config.db.user.find_one({"user_id": user_id})
                    if len(user_data["favorite"]) > 0:
                        message = flex_template.show_favorite(
                            restaurants=user_data["favorite"][:10]
                        )
                    else:
                        message = TextSendMessage(text="您的最愛列表內還沒有餐廳喔！")

                # 投票池
                elif user_message == "投票":
                    user_data = config.db.user.find_one({"user_id": user_id})
                    # 此處移除 LINE Notify 綁定限制
                    # 投票池內存在餐廳
                    if len(user_data["vote"]) > 0:
                        message = [
                            flex_template.show_vote_pull(
                                restaurants=user_data["vote"][:10]
                            ),
                            flex_template.create_vote(user_id=user_id),
                        ]
                    else:
                        message = TextSendMessage(text="您的投票池內還沒有餐廳喔！")

                # 測試創建投票
                elif user_message == "測試投票創建":
                    random_restaurants = config.db.restaurant.aggregate(
                        [{"$sample": {"size": 5}}]
                    )
                    restaurants = []
                    for each in random_restaurants:
                        restaurants.append(each["place_id"])
                    message = [
                        flex_template.show_vote_pull(restaurants=restaurants),
                        flex_template.create_vote(user_id="example"),
                    ]

                ## 測試投票
                elif user_message == "測試投票":
                    contents = flex_template.share_vote(pull_id="example")
                    message = FlexSendMessage(alt_text="使用教學", contents=contents)

                elif user_message == "測試投票結果":
                    pull_id = "example"
                    vote_info = show_result(pull_id=pull_id)

                    vote_name = vote_info["vote_name"]
                    best = vote_info["best"]
                    users = vote_info["users"]
                    total_user_count = vote_info["total_user_count"]

                    message = flex_template.vote_result(
                        pull_id=pull_id,
                        vote_name=vote_name,
                        best=best,
                        users=users,
                        total_user_count=total_user_count,
                    )
                # 客服
                elif user_message == "客服":
                    message = TextSendMessage(text="客服連結\nhttps://lin.ee/DsogwtP")

                # 找餐廳
                elif "@找" in user_message:
                    target = user_message.split("@找")[1]
                    message = search_info(query=target)

                elif "\n" in user_message:
                    contents_list = user_message.split("\n")
                    if (
                        len(contents_list) >= 3
                        and "maps.app.goo.gl" in contents_list[2]
                    ):
                        google_maps_url = contents_list[2].split(" ")[0]
                        query = parse_google_maps_url(url=google_maps_url)
                        if query:
                            message = search_info(query=query)
                else:
                    # 面對單一使用者
                    if event.source.type == "user":
                        message = TextSendMessage(
                            text="不好意思，我聽不懂你在說什麼呢QwQ\n如需要幫助，請輸入「客服」尋求幫忙"
                        )
                    else:
                        can_reply = False
                        message = None
        except Exception as e:
            sentry_sdk.capture_exception(e)
            config.console.print_exception()
            message = flex_template.error()
        if can_reply:
            line_bot_api.reply_message(reply_token, message)

    # 地點訊息
    elif isinstance(event.message, LocationMessage):
        try:
            lat = event.message.latitude
            lng = event.message.longitude

            # 預設類別
            restaurant_category = ["隨便", "日式", "中式", "西式"]
            quick_reply_items = [
                QuickReplyButton(
                    action=PostbackAction(
                        label=category,
                        display_text=category,
                        data=f"search_||_{lat},{lng}_||_{category}",
                    )
                )
                for category in restaurant_category
            ]

            # 動態類別
            dynamic_update_category = Weather().customized_category(
                latitude=lat, longitude=lng
            )
            temp_quick_reply_items = [
                QuickReplyButton(
                    action=PostbackAction(
                        label=category,
                        display_text=dynamic_update_category[category],
                        data=f"search_||_{lat},{lng}_||_{dynamic_update_category[category]}",
                    )
                )
                for category in list(dynamic_update_category.keys())
            ]

            quick_reply_items += temp_quick_reply_items
            quick_reply_items.append(
                QuickReplyButton(
                    action=PostbackAction(
                        label="其他",
                        display_text="其他",
                        data=f"search_||_{lat},{lng}_||_其他",
                    )
                )
            )
            message = TextSendMessage(
                text="請選擇餐廳類別",
                quick_reply=QuickReply(items=quick_reply_items),
            )
        except Exception as e:
            sentry_sdk.capture_exception(e)
            config.console.print_exception()
            message = flex_template.error()
        line_bot_api.reply_message(reply_token, message)


def search_info(query: str, page_token: str = ""):
    """搜尋特定餐廳

    Args:
        query (str): 餐廳名稱
    """
    restaurants = RestaurantInfo(page_token=page_token)
    restaurants.search(query=query)
    if len(restaurants.restaurants) == 0:
        message = TextSendMessage(text=f"很抱歉，我們找不到相關的餐廳😭")
    else:
        # Show first five restaurant
        message = flex_template.search_result(
            restaurants=restaurants.restaurants[:5],
        )
    return message


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
        message = flex_template.show_restaurant(
            user_latitude=latitude,
            user_longitude=longitude,
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


def parse_google_maps_url(url: str):
    """擷取Google Maps網頁資訊

    Args:
        url (str): Google Maps URL
    """
    origin_url = requests.get(url=url).url
    response = requests.get(url=f"{origin_url}&hl=zh-TW")

    soup = BeautifulSoup(response.content, "html.parser")
    meta_list = soup.find_all("meta")
    for meta in meta_list:
        if "property" in meta.attrs:
            name = meta.attrs["property"]
            if name == "og:title":
                info = meta.attrs["content"]
                return info
    return None
