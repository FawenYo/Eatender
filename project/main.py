import os

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

from API.router import api
from cron import cron
from line.handler import line_app
from view import view
from vote.view import vote

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
# View
app.include_router(view)
# LINE Bot
app.include_router(line_app)
# REST API
app.include_router(api)
# Vote System
app.include_router(vote)
# Cron Job
app.include_router(cron)


# 404 Not Found
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exec):
    return templates.TemplateResponse("404.html", context={"request": request})


if __name__ == "__main__":
    # Local WSGI: Uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        workers=4,
        log_level="info",
        access_log=True,
        use_colors=True,
        reload=True,
    )
