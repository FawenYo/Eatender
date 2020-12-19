import json
import sys

import requests
from flask import Blueprint, request, render_template

# 上層目錄import
sys.path.append(".")
import config

vote = Blueprint("vote", __name__)


@vote.route("/login")
def login():
    if "liff.state" in request.args:
        pull_id = request.args.get("liff.state")[1:]
    elif "id" in request.args:
        pull_id = request.args.get("id")
    else:
        pull_id = ""
    return render_template("login.html", pull_id=pull_id)


@vote.route("/vote")
def vote_page():
    pull_id = request.args.get("id")
    user_name = request.args.get("name")
    message = get_pull_data(pull_id=pull_id)
    if message["status"] == "success":
        return render_template(
            "restaurant.html", data=message["restaurants"], name=user_name
        )
    else:
        return message


@vote.route("/api/vote/<pull_id>", methods=["POST"])
def get_pull_data(pull_id):
    pull_data = config.db.vote_pull.find_one({"_id": pull_id})
    if pull_data:
        message = {"status": "success", "restaurants": pull_data["restaurants"]}
    else:
        message = {"status": "error", "error_message": "Vote pull not found."}
    return message


@vote.route("/vote/save", methods=["POST"])
def vote_save():
    # TODO: 和前端溝通
    return False


@vote.route("/SaveTimes.php", methods=["POST"])
def route_savetimes():
    post_data = request.form
    response = requests.post(
        "https://www.when2meet.com/SaveTimes.php", data=post_data
    ).text
    return response


@vote.route("/ProcessLogin.php", methods=["POST"])
def route_process_login():
    post_data = request.form
    response = requests.post(
        "https://www.when2meet.com/ProcessLogin.php", data=post_data
    ).text
    return response


@vote.route("/AvailabilityGrids.php", methods=["POST"])
def route_availability_grids():
    post_data = request.form
    response = requests.post(
        "https://www.when2meet.com/AvailabilityGrids.php", data=post_data
    ).text
    return response
