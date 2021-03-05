import sys
from datetime import datetime

import pytz
from linebot import LineBotApi
from linebot.models import *

from . import flex_template

sys.path.append(".")

import config

line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)


def handle_follow(event):
    """事件 - 新使用者加入Bot

    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#follow-event
    """
    reply_token = event.reply_token
    message = flex_template.welcome()
    line_bot_api.reply_message(reply_token, message)
    profile = line_bot_api.get_profile(event.source.user_id)
    display_name = profile.display_name
    now = datetime.now(tz=pytz.timezone("Asia/Taipei"))
    data = {
        "user_id": event.source.user_id,
        "display_name": display_name,
        "add_time": now,
        "favorite": [],
        "vote": [],
        "notify": {"status": False, "token": ""},
    }
    config.db.user.insert_one(data)


def handle_unfollow(event):
    """事件 - 新使用者封鎖Bot

    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#unfollow-event
    """
    config.db.user.delete_one({"user_id": event.source.user_id})


def handle_join(event):
    """事件 - 加入群組/房間

    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#join-event
    """
    if event.source.type == "group":
        user_id = event.source.group_id
        summary = line_bot_api.get_group_summary(user_id)
        display_name = summary.group_name
    else:
        user_id = event.source.room_id
        display_name = user_id
    now = datetime.now(tz=pytz.timezone("Asia/Taipei"))
    data = {
        "user_id": user_id,
        "display_name": display_name,
        "add_time": now,
        "favorite": [],
        "vote": [],
        "notify": {"status": False, "token": ""},
    }
    config.db.user.insert_one(data)


def handle_leave(event):
    """事件 - 離開群組/房間

    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#leave-event
    """
    if event.source.type == "group":
        user_id = event.source.group_id
    else:
        user_id = event.source.room_id
    config.db.user.delete_one({"user_id": user_id})
