from flask import Flask, render_template

from API.router import api
from config import console
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


if __name__ == "__main__":
    console.log("[bold magenta]Server Staring![/bold magenta] :fire: :fire:")
    app.run(threaded=True, port=5000)
