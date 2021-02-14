from pydantic import BaseModel
from typing import List, Dict


class SaveVoteRestaurant(BaseModel):
    pull_id: str  # 投票池 ID
    user_id: str  # 使用者 ID
    choose_result: Dict[str, List[int]] = {"love": [], "hate": []}  # 餐廳選擇


class SaveVoteDate(BaseModel):
    pull_id: str  # 投票池 ID
    user_id: str  # 使用者 ID
    dates: List[str] = ["YYYY/M/DD hh:mm"]  # 投票日期時間
