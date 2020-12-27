import os

import uvicorn
from API.router import api
from cron import cron
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from line.handler import line_app
from starlette.exceptions import HTTPException as StarletteHTTPException
from vote.view import vote

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(line_app)
app.include_router(api)
app.include_router(vote)
app.include_router(cron)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("home.html", context={"request": request})


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", context={"request": request})


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    # note that we set the 404 status explicitly
    return templates.TemplateResponse("404.html", context={"request": request})


if __name__ == "__main__":
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
