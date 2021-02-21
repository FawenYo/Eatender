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
    all_votes = config.db.vote_pull.find({})
    for each_vote in all_votes:
        vote_cronjob(
            event_id=each_vote["_id"],
            creator=each_vote["creator"],
            vote_end=each_vote["vote_end"],
        )
    return "Init done"


# Set up vote cron jobs
def vote_cronjob(event_id: str, creator: str, vote_end: datetime):
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        show_result,
        "date",
        args=[event_id, creator],
        run_date=vote_end,
        timezone=pytz.timezone("Asia/Taipei"),
    )
    scheduler.start()
    return True


# Push vote result via LINE Noitfy
def show_result(event_id: str, creator: str):
    user_data = config.db.user.find_one({"user_id": creator})
    access_token = user_data["notify"]["token"]
    # TODO: 投票結果
    message = "TODO"
    response = config.lotify_client.send_message(
        access_token=access_token, message=message
    )
    return response
