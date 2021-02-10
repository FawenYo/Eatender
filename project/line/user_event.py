import sys

from linebot import LineBotApi
from linebot.models import *

from .templates import Template

sys.path.append(".")

import config
import MongoDB.operation as database

line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)


def handle_follow(event):
    """事件 - 新使用者加入Bot

    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#follow-event
    """
    reply_token = event.reply_token
    message = Template().welcome()
    line_bot_api.reply_message(reply_token, message)
    profile = line_bot_api.get_profile(event.source.user_id)
    display_name = profile.display_name
    database.new_user(user_id=event.source.user_id, display_name=display_name)


def handle_unfollow(event):
    """事件 - 新使用者封鎖Bot

    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#unfollow-event
    """
    database.delete_user(user_id=event.source.user_id)
