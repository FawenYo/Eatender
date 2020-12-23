from datetime import datetime

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import APIRouter
from linebot import LineBotApi

from config import LINE_CHANNEL_ACCESS_TOKEN, db
from vote.main import gettime_attendant

cron = APIRouter()
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)


@cron.get("/init")
async def init_cron():
    all_votes = db.vote_pull.find({})
    for each_vote in all_votes:
        set_cronjob(
            creator=each_vote["creator"],
            vote_end=each_vote["end_date"],
            vote_link=each_vote["vote_link"],
        )
    return "Init done"


def set_cronjob(creator: str, vote_end: datetime, vote_link: str):
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        show_result(creator=creator, vote_link=vote_link),
        "date",
        run_date=vote_end,
        timezone=pytz.timezone("Asia/Taipei"),
    )
    scheduler.start()
    return True


def show_result(creator: str, vote_link: str):
    message = gettime_attendant(url=vote_link)
    line_bot_api.push_message(creator, message)
