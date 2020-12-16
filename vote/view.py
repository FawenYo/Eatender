import sys

from flask import Blueprint


# 上層目錄import
sys.path.append(".")
import config

vote = Blueprint("vote", __name__)


@vote.route("/vote/<pull_id>", methods=["POST"])
def pull_data(pull_id):
    pull_data = config.db.vote_pull.find_one({"_id": pull_id})
    if pull_data:
        message = {"status": "success", "restaurants": pull_data["restaurants"]}
    else:
        message = {"status": "error", "error_message": "Vote pull not found."}
    return message
