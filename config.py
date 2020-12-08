import os
from rich.console import Console

console = Console()

# LINE Bot 設定
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")

# Google Maps AP
GOOGLE_MAPS_APIKEY = os.environ.get("GOOGLE_MAPS_APIKEY")

# Swagger 文件
SWAGGER_TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "Gourmet Bot API docs",
        "description": "API for Gourmet Bot",
        "contact": {
            "responsibleOrganization": "FawenYo",
            "responsibleDeveloper": "FawenYo",
            "email": "b07607001@ntu.edu.tw",
        },
        "license": {
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT",
        },
        "version": "0.0.1",
    },
    "host": "line-gourmet.herokuapp.com",
    "basePath": "/api",
    "schemes": ["https", "http"],
    "operationId": "Gourmet Bot",
}
