from datetime import datetime

import config
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import APIRouter
from linebot import LineBotApi
from linebot.models import *
from vote.main import gettime_attendant

cron = APIRouter()
line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)


@cron.get("/init")
async def init_cron():
    all_votes = config.db.vote_pull.find({})
    for each_vote in all_votes:
        set_cronjob(
            event_id=each_vote["_id"],
            creator=each_vote["creator"],
            vote_end=each_vote["end_date"],
            vote_link=each_vote["vote_link"],
        )
    return "Init done"


def set_cronjob(event_id: str, creator: str, vote_end: datetime, vote_link: str):
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        show_result,
        "date",
        args=[event_id, creator, vote_link],
        run_date=vote_end,
        timezone=pytz.timezone("Asia/Taipei"),
    )
    scheduler.start()
    return True


def show_result(event_id: str, creator: str, vote_link: str):
    user_data = config.db.user.find_one({"user_id": creator})
    access_token = user_data["notify"]["token"]
    message = gettime_attendant(event_id=event_id, url=vote_link)
    response = config.lotify_client.send_message(
        access_token=access_token, message=message
    )
    return response
