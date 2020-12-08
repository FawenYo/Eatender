from flasgger import Swagger, swag_from
from flask import Flask, render_template

from config import SWAGGER_TEMPLATE, console
from line.handler import line_app

app = Flask(__name__, static_url_path="/static/")
swagger = Swagger(app, template=SWAGGER_TEMPLATE)
# Disable auto sort JSON data when API return values
app.config["JSON_SORT_KEYS"] = False
app.register_blueprint(line_app)


@app.route("/")
@swag_from("docs/index.yml")
def index():
    return render_template("home.html")


if __name__ == "__main__":
    console.log("[bold magenta]Server Staring![/bold magenta] :fire: :fire:")
    app.run(threaded=True, port=5000)
