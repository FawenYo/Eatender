import requests
from bs4 import BeautifulSoup


def create_event(event_name: str, dates: str, early_time: int, later_time: int):
    """建立 when2meet 投票

    Args:
        event_name (str): 投票名稱
        dates (str): 投票日期 (%Y-%m-%d), 多日期之間以 "|" 連結
        early_time (int): 最早時間(24小時制)
        later_time (int): 最晚時間(24小時制)

    Returns:
        [type]: [description]
    """
    data = {
        "NewEventName": event_name,
        "DateTypes": "SpecificDates",
        "PossibleDates": dates,
        "NoEarlierThan": early_time,
        "NoLaterThan": later_time,
        "TimeZone": "Asia/Taipei",
    }

    response = requests.post("https://www.when2meet.com/SaveNewEvent.php", data=data)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    attrs = soup.find("body").attrs
    event_id = attrs["onload"].replace("window.location='/", "")
    event_id.strip("'")
    return f"https://www.when2meet.com/{event_id}"
