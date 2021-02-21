import os

import uvicorn
from api.urls import api
from cron import cron
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from line.urls import line_app
from starlette.exceptions import HTTPException as StarletteHTTPException
from view import view
from vote.urls import vote
from weather.urls import weather

app = FastAPI()

origins = ["http://127.0.0.1:3000", "http://127.0.0.1:8001"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
# Weather
app.include_router(weather)
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
        host="127.0.0.1",
        port=port,
        workers=4,
        log_level="info",
        access_log=True,
        use_colors=True,
        reload=True,
    )
