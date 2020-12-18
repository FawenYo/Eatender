from MongoDB.operation import create_vote
from flask import Flask, render_template

from API.router import api
from line.handler import line_app
from vote.view import vote, pull_data

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


@app.route("/eatender")
@app.route("/eatender/<pull_id>")
def eatender(pull_id=""):
    message = pull_data(pull_id=pull_id)
    if message["status"] == "success":
        return render_template("restaurant.html", data=message["restaurants"])
    else:
        return message


@app.route("/test")
def test():
    return render_template("test.html")


@app.route("/card")
def card():
    return render_template("card.html")


if __name__ == "__main__":
    # Used only when running locally.
    app.run(threaded=True, port=8001, debug=True)
