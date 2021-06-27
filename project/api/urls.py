import config
import pandas as pd
import requests
from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse

api = APIRouter()


@api.get("/api/export/history")
async def export_history() -> FileResponse:
    """資料庫查詢記錄

    Returns:
        FileResponse: history.csv
    """
    data = pd.DataFrame()
    results = config.db.history.find({})
    for each in results:
        each["latitude"], each["longitude"] = each["location"]
        del each["location"]
        data = data.append(each, ignore_index=True)
    data.to_csv("history.csv", encoding="utf_8_sig")
    return FileResponse("history.csv")
