import random
import re
import string
import sys
import threading
from datetime import datetime

import sentry_sdk
from linebot import LineBotApi
from linebot.models import *

sys.path.append(".")

import config
import cron
import MongoDB.operation as database
from food.main import Restaurant_Info
from line.templates import Template
from vote.main import create_event
from weather.main import Weather

line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)


def handle_message(event):
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
                    if pending["action"] == "search":
                        config.db.pending.delete_one({"user_id": user_id})
                        latitude = pending["latitude"]
                        longitude = pending["longitude"]
                        message = find_nearby(
                            user_id=user_id,
                            latitude=latitude,
                            longitude=longitude,
                            keyword=user_message,
                        )

                    # 創建投票
                    else:
                        (
                            status,
                            event_name,
                            available_dates,
                            no_earlier,
                            no_later,
                        ) = parse_string(content=user_message)

                        if status:
                            config.db.pending.delete_one({"user_id": user_id})
                            user = config.db.user.find_one({"user_id": user_id})
                            user["vote"] = []
                            config.db.user.update_one(
                                {"user_id": user_id}, {"$set": user}
                            )

                            link = create_event(
                                event_name=event_name,
                                dates=available_dates,
                                early_time=no_earlier,
                                later_time=no_later,
                            )

                            vote_id = "".join(
                                random.choice(string.ascii_letters + string.digits)
                                for x in range(10)
                            )
                            database.create_vote(
                                creator=user_id,
                                vote_id=vote_id,
                                vote_link=link,
                                restaurants=pending["pools"],
                                end_date=pending["end_date"],
                            )
                            threading.Thread(
                                target=cron.vote_cronjob,
                                args=(vote_id, user_id, pending["end_date"], link),
                            ).start()
                            message = Template().share_vote(pull_id=vote_id)
                        else:
                            message = TextSendMessage(
                                text="抱歉，格式有誤，請重新輸入！\n如要取消操作請輸入 '取消' "
                            )

            # 文字訊息
            else:
                # 教學
                if user_message == "教學":
                    message = Template().tutorial()
                    line_bot_api.reply_message(reply_token, message)

                # 我的最愛
                if user_message == "我的最愛":
                    user_data = config.db.user.find_one({"user_id": user_id})
                    if len(user_data["favorite"]) > 0:
                        message = Template().show_favorite(
                            restaurants=user_data["favorite"][:10]
                        )
                    else:
                        message = TextSendMessage(text="您的最愛列表內還沒有餐廳喔！")

                # 投票池
                elif user_message == "投票":
                    user_data = config.db.user.find_one({"user_id": user_id})
                    # 已綁定 LINE Notify
                    if user_data["notify"]["status"]:
                        # 投票池內存在餐廳
                        if len(user_data["vote"]) > 0:
                            message = [
                                Template().show_vote_pull(
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
                        message = TextSendMessage(
                            text=f"尚未綁定 LINE Notify!\n請先前往 {config.SITE_NAME}notify/?uid={user_id} 進行綁定~"
                        )

                # 客服
                elif user_message == "客服":
                    message = TextSendMessage(text="客服連結\nhttps://lin.ee/DsogwtP")

                # 找餐廳
                elif "@找" in user_message:
                    target = user_message.split("@找")[1]
                    message = search_info(query=target)

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
            message = Template().error()
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
            dynamic_update_category = Weather().customized_category(lat=lat, lng=lng)
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
            message = Template().error()
        line_bot_api.reply_message(reply_token, message)


def search_info(query: str, page_token: str = ""):
    """搜尋特定餐廳

    Args:
        query (str): Query Info
    """
    restaurants = Restaurant_Info(page_token=page_token)
    restaurants.search(query=query)
    if len(restaurants.restaurants) == 0:
        message = TextSendMessage(text=f"很抱歉，我們找不到相關的餐廳😭")
    else:
        # Show first five restaurant
        message = Template().search_result(
            restaurants=restaurants.restaurants[:5],
        )
    # 記錄使用者位置
    """thread = threading.Thread(
        target=database.record_user_search, args=(user_id, latitude, longitude, keyword)
    )
    thread.start()"""
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
    restaurants = Restaurant_Info(
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


def parse_string(content: str):
    """投票資訊

    Args:
        content (str): create vote's message content
    """
    # default
    status = True
    event_name = ""
    available_dates = ""
    no_earlier = 0
    no_later = 24

    if not content:
        # input是空字串，回傳預設值
        status = False
        return status, event_name, available_dates, no_earlier, no_later

    try:
        date_candidates = re.findall(r"\d{4}-\d{1,2}-\d{1,2}", content)
        if len(date_candidates) == 1:
            date_candidates = date_candidates[0]
        elif len(date_candidates) > 1:
            date_candidates = "|".join(date_candidates)
        content = content.replace(date_candidates, "")

        event_name = content.replace(re.findall(r"//\d{1,2}/\d{1,2}", content)[0], "")
        daytime_constraint = re.findall(r"//(\d{1,2})/(\d{1,2})", content)[0]
        daytime_constraint = list(map(int, daytime_constraint))

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
            status = False
            pass

        no_earlier = min(daytime_constraint)
        no_later = max(daytime_constraint)
        if no_earlier < 0 or no_later > 24 or no_earlier == no_later:
            # 時間限制格式錯誤
            status = False
    except:
        status = False
        return status, event_name, available_dates, no_earlier, no_later

    return status, event_name, available_dates, no_earlier, no_later