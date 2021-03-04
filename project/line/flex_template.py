import json
import re
import sys
from datetime import datetime, timedelta

from linebot.models import FlexSendMessage

sys.path.append(".")
import config

true = True


def welcome() -> FlexSendMessage:
    """歡迎訊息

    Returns:
        FlexSendMessage: 歡迎使用 Eatender！
    """
    with open("line/model/welcome.json") as json_file:
        contents = json.load(json_file)
    message = FlexSendMessage(alt_text="歡迎使用 Eatender！", contents=contents)
    return message


def tutorial() -> FlexSendMessage:
    """使用教學

    Returns:
        FlexSendMessage: 使用教學
    """
    with open("line/model/tutorial.json") as json_file:
        contents = json.load(json_file)
    message = FlexSendMessage(alt_text="使用教學", contents=contents)
    return message


def share_vote(pull_id: str) -> dict:
    """WEB - 分享投票

    Args:
        pull_id (str): 投票池ID

    Returns:
        dict: 投票分享資訊
    """
    with open("line/model/share_vote.json") as json_file:
        contents = json.load(json_file)
    contents["footer"]["contents"][0]["contents"][0]["action"][
        "uri"
    ] = f"https://liff.line.me/1655422218-8n1PlOw1?pull_id={pull_id}"
    return contents


def not_bound(user_id: str) -> FlexSendMessage:
    """尚未綁定 LINE Notify

    Args:
        user_id (str): [description]

    Returns:
        FlexSendMessage: 尚未綁定 LINE Notify
    """
    with open("line/model/not_bound.json") as json_file:
        contents = json.load(json_file)
    contents["footer"]["contents"][0]["action"][
        "uri"
    ] = f"{config.SITE_NAME}notify/?uid={user_id}"
    message = FlexSendMessage(alt_text=f"尚未綁定 LINE Notify", contents=contents)
    return message


def show_vote_pull(restaurants) -> FlexSendMessage:
    """投票池列表

    Args:
        restaurants: 餐廳列表

    Returns:
        FlexSendMessage: 投票池列表
    """
    show_list = []
    for pid in restaurants:
        each = json.loads(config.cache.get(pid))
        place_id = each["place_id"]
        restaurant_name = each["name"]
        keywords = each["keywords"]
        photo_url = each["photo_url"]
        website = each["website"]
        ifoodie_url = each["ifoodie_url"]
        rating = each["rating"]
        price = each["price"]
        address = each["address"]
        phone_number = each["phone_number"]
        open_now = find_operating_status(data=each["operating_time"]["weekday_text"])

        card = vote_card(
            place_id=place_id,
            restaurant_name=restaurant_name,
            keywords=keywords,
            photo_url=photo_url,
            website=website,
            ifoodie_url=ifoodie_url,
            rating=rating,
            price=price,
            address=address,
            open_now=open_now,
            phone_number=phone_number,
        )
        show_list.append(card)
    contents = {
        "type": "carousel",
        "contents": show_list,
    }
    message = FlexSendMessage(alt_text="投票池列表", contents=contents)
    return message


def show_favorite(restaurants) -> FlexSendMessage:
    """最愛列表

    Args:
        restaurants: 餐廳列表

    Returns:
        FlexSendMessage: 最愛列表
    """
    show_list = []
    for each in restaurants:
        place_id = each["place_id"]
        restaurant_name = each["name"]
        keywords = each["keywords"]
        photo_url = each["photo_url"]
        website = each["website"]
        ifoodie_url = each["ifoodie_url"]
        rating = each["rating"]
        price = each["price"]
        address = each["address"]
        phone_number = each["phone_number"]
        lat = each["location"]["lat"]
        lng = each["location"]["lng"]
        open_now = find_operating_status(data=each["operating_time"]["weekday_text"])

        card = restaurant_card_info(
            place_id=place_id,
            restaurant_name=restaurant_name,
            keywords=keywords,
            photo_url=photo_url,
            website=website,
            ifoodie_url=ifoodie_url,
            rating=rating,
            price=price,
            address=address,
            open_now=open_now,
            phone_number=phone_number,
            lat=lat,
            lng=lng,
        )
        show_list.append(card)
    contents = {
        "type": "carousel",
        "contents": show_list,
    }
    message = FlexSendMessage(alt_text="最愛列表", contents=contents)
    return message


def show_restaurant(
    restaurants,
    user_latitude: float = 0.0,
    user_longitude: float = 0.0,
    keyword: str = "",
    next_page: str = "",
) -> FlexSendMessage:
    """附近餐廳列表

    Args:
        restaurants: 餐廳列表
        user_latitude (float, optional): 使用者緯度. Defaults to 0.0.
        user_longitude (float, optional): 使用者經度. Defaults to 0.0.
        keyword (str, optional): 餐廳關鍵字. Defaults to "".
        next_page (str, optional): 更多餐廳 token. Defaults to "".

    Returns:
        FlexSendMessage: 餐廳資訊列表
    """
    show_list = []
    for each in restaurants:
        place_id = each.place_id
        restaurant_name = each.name
        keywords = each.keywords
        photo_url = each.photo_url
        website = each.website
        ifoodie_url = each.ifoodie_url
        rating = each.rating
        price = each.price
        address = each.address
        open_now = each.open_now
        phone_number = each.phone_number
        lat = each.location["lat"]
        lng = each.location["lng"]
        card = restaurant_card_info(
            place_id=place_id,
            restaurant_name=restaurant_name,
            keywords=keywords,
            photo_url=photo_url,
            website=website,
            ifoodie_url=ifoodie_url,
            rating=rating,
            price=price,
            address=address,
            open_now=open_now,
            phone_number=phone_number,
            lat=lat,
            lng=lng,
        )
        show_list.append(card)
    contents = {
        "type": "carousel",
        "contents": show_list,
    }
    if next_page:
        more = show_more(
            user_latitude=user_latitude,
            user_longitude=user_longitude,
            keyword=keyword,
            next_page=next_page,
        )
        contents["contents"].append(more)
    message = FlexSendMessage(alt_text="餐廳資訊列表", contents=contents)
    return message


def create_vote(user_id: str) -> FlexSendMessage:
    """投票創建確認

    Args:
        user_id (str): 使用者 ID

    Returns:
        FlexSendMessage: 投票創建確認
    """
    with open("line/model/create_vote.json") as json_file:
        contents = json.load(json_file)
    contents["footer"]["contents"][0]["action"][
        "uri"
    ] = f"https://liff.line.me/1655422218-leDE61nD?user_id={user_id}"
    message = FlexSendMessage(alt_text="投票創建確認", contents=contents)
    return message


def vote_result(
    pull_id: str, vote_name: str, best: list, users: list, total_user_count: int
) -> FlexSendMessage:
    """投票結果

    Args:
        pull_id (str): 投票池ID
        vote_name (str): 投票名稱
        best (list): 投票結果
        users (list): 與會人列表
        total_user_count (int): 投票總人數

    Returns:
        FlexSendMessage: 投票結果
    """
    with open("line/model/vote_result.json") as json_file:
        contents = json.load(json_file)
    contents["body"]["contents"][1]["text"] = vote_name
    contents["body"]["contents"][2]["text"] = f"共{total_user_count}人參與投票"
    for each in best:
        restaurant_name = each["restaurant"]["name"]
        date_text = each["date"]
        session_text = each["session"]

        template = {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": restaurant_name,
                            "align": "center",
                            "size": "lg",
                            "weight": "bold",
                            "margin": "md",
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": date_text,
                                    "size": "sm",
                                    "weight": "bold",
                                    "align": "start",
                                    "offsetStart": "10px",
                                },
                                {
                                    "type": "text",
                                    "text": session_text,
                                    "align": "end",
                                    "size": "sm",
                                    "color": "#F26013",
                                    "margin": "none",
                                    "weight": "bold",
                                    "offsetEnd": "10px",
                                },
                            ],
                            "margin": "lg",
                        },
                    ],
                    "paddingAll": "none",
                    "borderWidth": "none",
                    "cornerRadius": "10px",
                    "borderColor": "#F7F1C7",
                    "margin": "none",
                }
            ],
            "margin": "md",
            "borderColor": "#F7F1C7",
            "borderWidth": "medium",
            "cornerRadius": "10px",
            "paddingBottom": "10px",
        }
        contents["body"]["contents"][5]["contents"].append(template)
    for each_user in users:
        template = {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "【",
                            "margin": "none",
                            "size": "md",
                            "align": "start",
                            "offsetStart": "none",
                            "flex": 0,
                        },
                        {"type": "text", "text": each_user, "align": "center"},
                        {"type": "text", "text": "】", "align": "end", "flex": 0},
                    ],
                }
            ],
            "margin": "md",
        }
        contents["body"]["contents"][8]["contents"].append(template)
    contents["footer"]["contents"][0]["contents"][0]["action"][
        "uri"
    ] = f"https://liff.line.me/1655422218-KOeZvV1e?pull_id={pull_id}"
    message = FlexSendMessage(alt_text="投票結果", contents=contents)
    return message


# 店家營業狀態
def find_operating_status(data):
    now = datetime.now()
    today_date = now.strftime("%Y:%m:%d")
    time = now.strftime("%H:%M")

    today_open = data[now.weekday()].split(",")
    for each in today_open:
        if "休息" in each:
            return False
        if "24 小時營業" in each:
            return False
        temp = re.findall(r"\d{1,2}\:\d{1,2}", each)
        start = datetime.strptime(f"{today_date}:{temp[0]}", "%Y:%m:%d:%H:%M")
        current = datetime.strptime(f"{today_date}:{time}", "%Y:%m:%d:%H:%M")
        end = datetime.strptime(f"{today_date}:{temp[1]}", "%Y:%m:%d:%H:%M")
        if int(temp[0][0:2]) > int(temp[1][0:2]):
            end += timedelta(days=1)

        if start <= current <= end:
            return True
    return False


def restaurant_card_info(
    place_id: str,
    restaurant_name: str,
    keywords: list,
    photo_url: str,
    website: str,
    ifoodie_url: str,
    rating: float,
    price: int,
    address: str,
    open_now: bool,
    phone_number: str,
    lat: float,
    lng: float,
) -> dict:
    """卡片模板 - 附近餐廳資訊

    Args:
        place_id (str): Google Maps' place id
        restaurant_name (str): 餐廳名稱
        keywords (list): 餐廳評論列表
        photo_url (str): 餐廳照片
        website (str): 餐廳網站連結
        ifoodie_url (str): 餐廳愛食記連結
        rating (float): Google Maps' 評分
        price (int): 餐廳平均消費價格
        address (str): 餐廳地址
        open_now (bool): 是否營業中
        phone_number (str): 餐廳電話
        lat (float): 使用者緯度
        lng (float): 使用者經度

    Returns:
        dict: Flex Message 卡片模板
    """
    star_list = stars_template(rating=rating)
    if price == 0:
        price = "N/A"
    comments = keywords_template(keywords=keywords)
    operate_status, operate_color = operate_status_template(open_now=open_now)

    with open("line/model/restaurant_card_info.json") as json_file:
        card = json.load(json_file)
    card["header"]["contents"][0]["contents"][0]["url"] = photo_url
    card["header"]["contents"][0]["contents"][1]["contents"] = [operate_status]
    card["header"]["contents"][0]["contents"][1]["backgroundColor"] = operate_color
    card["body"]["contents"][0]["contents"][0]["text"] = restaurant_name
    card["body"]["contents"][1]["contents"] = star_list + [
        {
            "type": "text",
            "text": str(rating),
            "size": "sm",
            "color": "#999999",
            "margin": "sm",
            "flex": 0,
        },
    ]
    card["body"]["contents"][2]["contents"][0]["text"] = f"${price}"
    card["body"]["contents"][2]["contents"][1]["action"]["uri"] = website
    card["body"]["contents"][2]["contents"][2]["action"]["uri"] = ifoodie_url
    detail = [
        {
            "type": "text",
            "text": "評論",
            "size": "sm",
            "color": "#999999",
            "flex": 0,
        }
    ]
    detail.extend(comments)
    card["body"]["contents"][3]["contents"] = detail
    card["body"]["contents"][4]["contents"][0]["contents"][1]["text"] = address
    card["body"]["contents"][4]["contents"][1]["contents"][1]["text"] = phone_number
    card["footer"]["contents"][0]["contents"][0]["action"][
        "uri"
    ] = f"https://www.google.com/maps/search/?api=1&query={lat},{lng}&travelmode=walking"
    card["footer"]["contents"][0]["contents"][1]["action"][
        "data"
    ] = f"favorite_||_{place_id}"
    card["footer"]["contents"][1]["contents"][0]["action"][
        "data"
    ] = f"vote_||_{place_id}"
    print(len(card["body"]["contents"][3]["contents"]))
    with open("test.json", "w") as f:
        json.dump(card, f)
    return card


def show_more(
    user_latitude: float, user_longitude: float, keyword: str, next_page: str
) -> dict:
    """顯示更多餐廳

    Args:
        user_latitude (float): 使用者緯度
        user_longitude (float): 使用者經度
        keyword (str): 餐廳搜尋關鍵字
        next_page (str): 更多餐廳 token

    Returns:
        dict: 顯示更多 template
    """
    with open("line/model/show_more.json") as json_file:
        card = json.load(json_file)
    card["body"]["contents"][2]["contents"][0]["action"][
        "data"
    ] = f"more_||_{user_latitude},{user_longitude}_||_{keyword}_||_{next_page}"
    return card


def vote_card(
    place_id: str,
    restaurant_name: str,
    keywords: list,
    photo_url: str,
    website: str,
    ifoodie_url: str,
    rating: float,
    price: int,
    address: str,
    open_now: bool,
    phone_number: str,
) -> dict:
    """卡片模板 - 投票餐廳資訊

    Args:
        place_id (str): Google Maps' place id
        restaurant_name (str):餐廳名稱
        keywords (list): 餐廳評論列表
        photo_url (str): 餐廳照片
        website (str): 餐廳網站連結
        ifoodie_url (str): 餐廳愛食記連結
        rating (float): Google Maps' 評分
        price (int): 餐廳平均消費價格
        address (str): 餐廳地址
        open_now (bool): 是否營業中
        phone_number (str): 餐廳電話

    Returns:
        dict: Flex Message 卡片模板
    """
    star_list = stars_template(rating=rating)
    if price == 0:
        price = "N/A"
    comments = keywords_template(keywords=keywords)
    operate_status, operate_color = operate_status_template(open_now=open_now)

    with open("line/model/vote_card.json") as json_file:
        card = json.load(json_file)
    card["header"]["contents"][0]["contents"][0]["url"] = photo_url
    card["header"]["contents"][0]["contents"][1]["contents"] = [operate_status]
    card["header"]["contents"][0]["contents"][1]["backgroundColor"] = operate_color
    card["body"]["contents"][0]["contents"][0]["text"] = restaurant_name
    card["body"]["contents"][1]["contents"] = star_list + [
        {
            "type": "text",
            "text": str(rating),
            "size": "sm",
            "color": "#999999",
            "margin": "sm",
            "flex": 0,
        },
    ]
    card["body"]["contents"][2]["contents"][0]["text"] = f"${price}"
    card["body"]["contents"][2]["contents"][1]["action"]["uri"] = website
    card["body"]["contents"][2]["contents"][2]["action"]["uri"] = ifoodie_url
    detail = [
        {
            "type": "text",
            "text": "評論",
            "size": "sm",
            "color": "#999999",
            "flex": 0,
        }
    ]
    detail.extend(comments)
    card["body"]["contents"][3]["contents"] = detail
    card["body"]["contents"][4]["contents"][0]["contents"][1]["text"] = address
    card["body"]["contents"][4]["contents"][1]["contents"][1]["text"] = phone_number
    card["footer"]["contents"][0]["contents"][0]["action"][
        "data"
    ] = f"remove_||_{place_id}"
    return card


def error() -> FlexSendMessage:
    """發生錯誤

    Returns:
        FlexSendMessage: 發生錯誤！
    """
    with open("line/model/error.json") as json_file:
        contents = json.load(json_file)
    message = FlexSendMessage(alt_text="發生錯誤！", contents=contents)
    return message


def operate_status_template(open_now: bool) -> tuple:
    """Flex Message 餐廳營業狀況

    Args:
        open_now (bool): 營業中

    Returns:
        tuple: (營業狀況, 營業文字顏色)
    """
    if open_now:
        operate_status = {
            "type": "text",
            "text": "營業中",
            "size": "xs",
            "color": "#ffffff",
            "align": "center",
            "gravity": "center",
        }
        operate_color = "#9ACD32"
    else:
        operate_status = {
            "type": "text",
            "text": "休息中",
            "size": "xs",
            "color": "#ffffff",
            "align": "center",
            "gravity": "center",
        }
        operate_color = "#FF6347"
    return (operate_status, operate_color)


def stars_template(rating: float) -> list:
    """Flex Message 星星圖示

    Args:
        rating (float): 餐廳 Google Maps 評價

    Returns:
        list: 星星圖示
    """
    star = {
        "type": "icon",
        "size": "sm",
        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
    }
    grey_star = {
        "type": "icon",
        "size": "sm",
        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
    }
    star_list = int(rating) * [star] + (5 - int(rating)) * [grey_star]
    return star_list


def keywords_template(keywords: list) -> list:
    """Flex Message 留言關鍵字

    Args:
        keywords (list): 關鍵字列表

    Returns:
        list: 關鍵字
    """
    comments = []
    for each in keywords:
        data = {
            "type": "text",
            "text": each,
            "flex": 0,
            "margin": "xl",
            "size": "sm",
            "color": "#999999",
        }
        comments.append(data)
    return comments
