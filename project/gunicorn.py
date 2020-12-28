import os

# Gunicorn settings
port = int(os.getenv("PORT", 8001))
bind = f"0.0.0.0:{port}"
loglevel = "debug"
workers = 4
threads = 4
