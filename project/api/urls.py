import pandas as pd
import requests
from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse

import config

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


@api.get("/api/deploy", response_class=JSONResponse)
async def deploy() -> JSONResponse:
    """LINE Notify通知 Git development分支 commit內容

    Returns:
        JSONResponse: 通知結果
    """
    commit_info = requests.get(config.GITHUB_REPO_URL).json()
    commit_committer = commit_info["commit"]["commit"]["committer"]["name"]
    commit_date = commit_info["commit"]["commit"]["committer"]["date"]
    commit_message = commit_info["commit"]["commit"]["message"]
    commit_url = commit_info["commit"]["html_url"]
    for token in config.AUTHORS_NOTIFY_TOKEN:
        message = f"New Commit\n提交者：{commit_committer}\n提交日期：{commit_date}\n提交訊息：{commit_message}\n詳細資訊：{commit_url}"
        config.lotify_client.send_message(access_token=token, message=message)
    return JSONResponse(content={"status": "success"})
