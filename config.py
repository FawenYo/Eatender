import os

from rich.console import Console

console = Console()

# LINE Bot 設定
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")

# Google Maps AP
GOOGLE_MAPS_APIKEY = os.environ.get("GOOGLE_MAPS_APIKEY")
