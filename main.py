from flask import Flask, render_template, request

from API.router import api
from line.handler import line_app
from MongoDB.operation import create_vote
from vote.view import pull_data, vote

app = Flask(__name__, static_url_path="/static/")
# Disable auto sort JSON data when API return values
app.config["JSON_SORT_KEYS"] = False
# Return proper json format data
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.register_blueprint(line_app)
app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(vote)


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/vote")
def vote():
    pull_id = request.args.get("id")
    user_name = request.args.get("name")
    if not pull_id and not user_name:
        state = request.args.get("liff.state")
        state = state.replace("?", "")
        args = state.split("&")
        for each in args:
            key, value = each.split("=")
            if key == "id":
                pull_id = value
            elif key == "name":
                user_name = value
    message = pull_data(pull_id=pull_id)
    if message["status"] == "success":
        return render_template(
            "restaurant.html", data=message["restaurants"], name=user_name
        )
    else:
        return message


@app.route("/create")
def create():
    return render_template("create.html")


@app.route("/choose")
def choose():
    return render_template("choose.html", name="test")


if __name__ == "__main__":
    # Used only when running locally.
    app.run(threaded=True, port=8001, debug=True)
