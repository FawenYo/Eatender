from typing import Dict, List

from pydantic import BaseModel

weekday_text = {
    0: "（一）",
    1: "（二）",
    2: "（三）",
    3: "（四）",
    4: "（五）",
    5: "（六）",
    6: "（日）",
}


class CreateVote(BaseModel):
    user_id: str  # 使用者 ID
    vote_name: str  # 投票名稱
    due_date: str  # 投票截止 (LINE) 日期
    date_range: List[dict] = [
        {"year": 2021, "month": 3, "day": 5},
    ]  # 投票日期
    time_session: List[str]  # 投票時段


class SaveVoteRestaurant(BaseModel):
    pull_id: str  # 投票池 ID
    user_id: str  # 使用者 ID
    choose_result: Dict[str, List[str]] = {"love": [], "nope": []}  # 餐廳選擇


class OldSaveVoteDate(BaseModel):
    pull_id: str  # 投票池 ID
    user_id: str  # 使用者 ID
    dates: List[str] = ["YYYY/M/DD hh:mm"]  # 投票日期時間


class SaveVoteDate(BaseModel):
    pull_id: str  # 投票池 ID
    user_id: str  # 使用者 ID
    available_date: Dict[str, str] = {"2021/12/31 (日) 午餐": "ok"}  # 投票日期時間
