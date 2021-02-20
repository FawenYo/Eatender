from pydantic import BaseModel
from typing import List, Dict


class CreateVote(BaseModel):
    user_id: str  # 使用者 ID
    vote_name: str  # 投票名稱
    vote_end: str  # 投票截止 (LINE) 日期
    start_date: str  # 投票開始日期
    num_days: int  # 投票日期天數
    min_time: int  # 最早時間
    max_time: int  # 最晚時間


class SaveVoteRestaurant(BaseModel):
    pull_id: str  # 投票池 ID
    user_id: str  # 使用者 ID
    choose_result: Dict[str, List[int]] = {"love": [], "hate": []}  # 餐廳選擇


class SaveVoteDate(BaseModel):
    pull_id: str  # 投票池 ID
    user_id: str  # 使用者 ID
    dates: List[str] = ["YYYY/M/DD hh:mm"]  # 投票日期時間
