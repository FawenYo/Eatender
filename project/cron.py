from datetime import datetime

import config
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import APIRouter
from linebot import LineBotApi
from linebot.models import *

cron = APIRouter()
line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)


# Load cron jobs from database
@cron.get("/init")
async def init_cron():
    all_votes = config.db.vote.find({})
    for each_vote in all_votes:
        vote_cronjob(
            event_id=each_vote["_id"],
            creator=each_vote["creator"],
            due_date=each_vote["due_date"],
        )
    return "Init done"


# Set up vote cron jobs
def vote_cronjob(event_id: str, creator: str, due_date: str):
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        show_result,
        "date",
        args=[event_id, creator],
        run_date=f"{due_date}",
        timezone=pytz.timezone("Asia/Taipei"),
    )
    scheduler.start()
    return True


# Push vote result via LINE Noitfy
def show_result(event_id: str, creator: str):
    # TODO: 投票結果
    message = "TODO"
    line_bot_api.push_message(creator, message)
    return "ok"
