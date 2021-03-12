import config
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from dateutil import parser
from fastapi import APIRouter
from line import flex_template
from linebot import LineBotApi
from linebot.models import *
from munch import munchify
from vote.urls import show_result

cron = APIRouter()
line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)


# Load cron jobs from database
@cron.get("/init")
async def init_cron():
    all_votes = config.db.vote.find({})
    for each_vote in all_votes:
        vote_cronjob(
            pull_id=each_vote["_id"],
            creator=each_vote["creator"],
            due_date=each_vote["due_date"],
        )
    return "Init done"


# Set up vote cron jobs
def vote_cronjob(pull_id: str, creator: str, due_date: str):
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        send_result,
        "date",
        args=[pull_id, creator],
        run_date=parser.parse(due_date),
        timezone=pytz.timezone("Asia/Taipei"),
    )
    scheduler.start()
    return True


# Push vote result via LINE Noitfy
def send_result(pull_id: str, creator: str):
    vote_info = show_result(pull_id=pull_id)

    vote_name = vote_info["vote_name"]
    best = vote_info["best"]
    users = vote_info["users"]
    total_user_count = vote_info["total_user_count"]

    restaurants = []
    for each in best:
        i = munchify(each)
        if i.restaurant not in restaurants:
            restaurants.append(i.restaurant)
    message = [
        flex_template.vote_result(
            pull_id=pull_id,
            vote_name=vote_name,
            best=best,
            users=users,
            total_user_count=total_user_count,
        ),
        flex_template.show_restaurant(restaurants=restaurants),
    ]
    line_bot_api.push_message(creator, message)
