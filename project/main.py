from flask import Flask, render_template, request

from API.router import api
from line.handler import line_app
from vote.view import vote

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


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("404.html"), 404


if __name__ == "__main__":
    # Used only when running locally.
    app.run(threaded=True, host="0.0.0.0", port=8001, debug=True)
