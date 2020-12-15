from flask import Flask, render_template

from API.router import api
from line.handler import line_app

app = Flask(__name__, static_url_path="/static/")
# Disable auto sort JSON data when API return values
app.config["JSON_SORT_KEYS"] = False
# Return proper json format data
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.register_blueprint(line_app)
app.register_blueprint(api, url_prefix="/api")


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/eatender")
def eatender():
    return render_template("restaurant.html")


if __name__ == "__main__":
    # Used only when running locally.
    app.run(threaded=True, port=8001, debug=True)
