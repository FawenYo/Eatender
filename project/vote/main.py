import re
import sys
from collections import Counter

import requests
from bs4 import BeautifulSoup

# 上層目錄import
sys.path.append(".")
import config


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
    if event_id[-1] == "'":
        event_id = event_id[:-1]
    return f"https://www.when2meet.com/{event_id}"


def gettime_attendant(event_id: str, url: str):
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    raw_date = soup.find_all(
        "div",
        attrs={
            "style": [
                "display:inline-block;*display:inline;zoom:1;text-align:center;font-size:10px;width:44px;padding-right:1px;",
                "display:inline-block;*display:inline;zoom:1;text-align:center;font-size:10px;width:44px;padding-right:1px;margin-right:10px;",
            ]
        },
    )
    dates = []
    for each in raw_date:
        dates.append(
            str(each)
            .replace(
                '<div style="display:inline-block;*display:inline;zoom:1;text-align:center;font-size:10px;width:44px;padding-right:1px;margin-right:10px;">',
                "",
            )
            .replace(
                '<div style="display:inline-block;*display:inline;zoom:1;text-align:center;font-size:10px;width:44px;padding-right:1px;">',
                "",
            )
            .replace(
                '<br/><div style="display:inline-block;*display:inline;zoom:1;font-size:16px;">',
                "",
            )
            .replace("</div>", "")
        )
    dates = list(dict.fromkeys(dates))
    for i in range(len(dates)):
        dates[i] = dates[i].replace("  ", " ")
        dates[i] = f"{dates[i][:len(dates[i]) - 3]}, {dates[i][len(dates[i]) - 3:]}"

    time_template = {
        "Midnight": 0,
        "1 AM": 1,
        "2 AM": 2,
        "3 AM": 3,
        "4 AM": 4,
        "5 AM": 5,
        "6 AM": 6,
        "7 AM": 7,
        "8 AM": 8,
        "9 AM": 9,
        "10 AM": 10,
        "11 AM": 11,
        "Noon": 12,
        "1 PM": 13,
        "2 PM": 14,
        "3 PM": 15,
        "4 PM": 16,
        "5 PM": 17,
        "6 PM": 18,
        "7 PM": 19,
        "8 PM": 20,
        "9 PM": 21,
        "10 PM": 22,
        "11 PM": 23,
    }
    raw_times = soup.find_all(
        "div",
        attrs={
            "style": "text-align:right;width:44px;font-size:10px;margin:4px 4px 0px 0px;"
        },
    )
    times = []
    for each in raw_times:
        each = re.findall(
            r"<div style=\"text-align:right;width:44px;font-size:10px;margin:4px 4px 0px 0px;\">(.*?)</div>",
            str(each),
        )
        if not each:
            continue
        this = each[0].strip("\xa0")
        if this in time_template.keys():
            this = time_template[this]
            times.append(this)
    times = list(dict.fromkeys(times))

    group_grid = []
    for i in range(len(dates)):
        group_grid.append([[] for j in range((len(times) * 4))])

    raw_attendant = re.findall(
        r"PeopleNames\[\d\] = '(.*?)';PeopleIDs\[\d\] = (.*?);", str(response.text)
    )
    raw_attendant = list(dict.fromkeys(raw_attendant))
    attendant = dict()
    for each in raw_attendant:
        attendant[each[1]] = each[0]

    availables = re.findall(
        r"AvailableAtSlot\[(\d*?)\]\.push\((\d*?)\);", str(response.text)
    )
    availables = list(dict.fromkeys(availables))

    for each in availables:
        time_slot = int(each[0]) % (len(times) * 4)
        date_slot = int(each[0]) // (len(times) * 4)
        group_grid[date_slot][time_slot].append(str(each[1]))

    grid_count = []
    for each in group_grid:
        grid_count.append(list(map(len, each)))

    datetimes = dict()
    for i in range(len(group_grid)):
        for j in range(len(group_grid[i])):
            attendant_name = tuple(map(lambda s: attendant[s], group_grid[i][j]))
            if attendant_name not in datetimes.keys() and attendant_name:
                datetimes[attendant_name] = dict()
                datetimes[attendant_name][dates[i]] = list()
            elif attendant_name:
                datetimes[attendant_name][dates[i]] = list()

    for i in range(len(group_grid)):
        for j in range(len(group_grid[i])):
            attendant_name = tuple(map(lambda s: attendant[s], group_grid[i][j]))
            try:
                if attendant_name:
                    datetimes[attendant_name][dates[i]].append(j)
            except:
                pass
    try:
        group_amount = list(map(len, dict.fromkeys(datetimes)))
        max_people = max(group_amount)
    except ValueError:
        return "還沒有人投票哦！"

    result = dict()
    for i, amount in enumerate(group_amount):
        if amount == max_people:
            for j, datetime in enumerate(datetimes):
                if i == j:
                    result[datetime] = datetimes[datetime]

    def time_segment(raw_time: list):
        time_dict = {
            0: "00:00",
            1: "00:15",
            2: "00:30",
            3: "00:45",
            4: "01:00",
            5: "01:15",
            6: "01:30",
            7: "01:45",
            8: "02:00",
            9: "02:15",
            10: "02:30",
            11: "02:45",
            12: "03:00",
            13: "03:15",
            14: "03:30",
            15: "03:45",
            16: "04:00",
            17: "04:15",
            18: "04:30",
            19: "04:45",
            20: "05:00",
            21: "05:15",
            22: "05:30",
            23: "05:45",
            24: "06:00",
            25: "06:15",
            26: "06:30",
            27: "06:45",
            28: "07:00",
            29: "07:15",
            30: "07:30",
            31: "07:45",
            32: "08:00",
            33: "08:15",
            34: "08:30",
            35: "08:45",
            36: "09:00",
            37: "09:15",
            38: "09:30",
            39: "09:45",
            40: "10:00",
            41: "10:15",
            42: "10:30",
            43: "10:45",
            44: "11:00",
            45: "11:15",
            46: "11:30",
            47: "11:45",
            48: "12:00",
            49: "12:15",
            50: "12:30",
            51: "12:45",
            52: "13:00",
            53: "13:15",
            54: "13:30",
            55: "13:45",
            56: "14:00",
            57: "14:15",
            58: "14:30",
            59: "14:45",
            60: "15:00",
            61: "15:15",
            62: "15:30",
            63: "15:45",
            64: "16:00",
            65: "16:15",
            66: "16:30",
            67: "16:45",
            68: "17:00",
            69: "17:15",
            70: "17:30",
            71: "17:45",
            72: "18:00",
            73: "18:15",
            74: "18:30",
            75: "18:45",
            76: "19:00",
            77: "19:15",
            78: "19:30",
            79: "19:45",
            80: "20:00",
            81: "20:15",
            82: "20:30",
            83: "20:45",
            84: "21:00",
            85: "21:15",
            86: "21:30",
            87: "21:45",
            88: "22:00",
            89: "22:15",
            90: "22:30",
            91: "22:45",
            92: "23:00",
            93: "23:15",
            94: "23:30",
            95: "23:45",
        }

        base_time = times[0] * 4
        all_day_time = []
        time_session = f"{time_dict[base_time + raw_time[0]]}"

        for i in range(len(raw_time)):
            this_time = base_time + raw_time[i]
            if i < len(raw_time) - 1 and raw_time[i] + 1 == raw_time[i + 1]:
                continue
            else:
                time_session += f"~{time_dict[this_time + 1]}"
                all_day_time.append(time_session)
                if i < len(raw_time) - 1:
                    time_session = f"{time_dict[base_time + raw_time[i + 1]]}"

        return all_day_time

    wrapped_result = {
        "event_name": str(
            re.findall(r"<title>(.*?) - When2meet</title>", str(soup))[0]
        ),
        "candidates": [],
    }

    for key_1, item_1 in result.items():
        candidate = {
            "participants": key_1,
            "available_time": list(),
        }
        for key_2, item_2 in item_1.items():
            this_date = dict()
            this_date["date"] = key_2
            this_date["time"] = time_segment(result[key_1][key_2])
            candidate["available_time"].append(this_date)

        wrapped_result["candidates"].append(candidate)

    # 餐廳選擇結果
    choose_result = ""
    like_list = []
    event_data = config.db.vote_pull.find_one({"_id": event_id})
    for each_participant, like in event_data["participants"].items():
        like_list += like
    occurence_count = Counter(like_list)
    for restaurant_index, count in occurence_count.most_common(3):
        restaurant_name = event_data["restaurants"][restaurant_index]["name"]
        choose_result += f"{restaurant_name} ： {count}票\n"

    message = f'投票結果出爐啦！\n\n【{wrapped_result["event_name"]}】\n------------------\n{choose_result}'
    for each in wrapped_result["candidates"]:
        message += f'參與者：{each["participants"]}\n'
        for each_available in each["available_time"]:
            message += f'日期：{each_available["date"]}\n'
            message += f"時間："
            for i, each_time in enumerate(each_available["time"]):
                if i == 0:
                    message += f"{each_time}\n"
                else:
                    message += f"------{each_time}\n"
            message += "------------------\n"

    return message
