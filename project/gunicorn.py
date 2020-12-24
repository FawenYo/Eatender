import os

port = int(os.getenv("PORT", 8001))
bind = f"0.0.0.0:{port}"
loglevel = "debug"
workers = 4
threads = 4
reload = True
