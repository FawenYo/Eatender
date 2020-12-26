import re
from datetime import datetime, timedelta

from config import console
from linebot.models import FlexSendMessage

true = True


class Template:
    def __init__(self, user_lat=0, user_lng=0):
        self.user_lat = user_lat
        self.user_lng = user_lng

    def welcome(self):
        contents = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "image",
                        "size": "full",
                        "aspectMode": "cover",
                        "aspectRatio": "2:2.9",
                        "gravity": "center",
                        "url": "https://i.imgur.com/oy86bfe.jpg",
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "Eatender",
                                        "gravity": "top",
                                        "align": "center",
                                        "weight": "regular",
                                        "size": "3xl",
                                    }
                                ],
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "加LINE約吃飯，感情不會散",
                                        "size": "md",
                                        "margin": "md",
                                        "weight": "bold",
                                        "align": "center",
                                        "color": "#ffffffcc",
                                    }
                                ],
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "歡迎使用Eatender，",
                                        "weight": "bold",
                                        "color": "#666666",
                                        "size": "md",
                                        "margin": "lg",
                                    },
                                    {
                                        "type": "text",
                                        "text": "馬上開始第一次「約食」吧！",
                                        "weight": "bold",
                                        "color": "#666666",
                                        "size": "md",
                                        "margin": "xs",
                                        "offsetEnd": "0px",
                                    },
                                ],
                            },
                        ],
                        "backgroundColor": "#fdbe29cc",
                        "paddingAll": "30px",
                        "position": "absolute",
                        "offsetBottom": "0px",
                        "offsetStart": "0px",
                        "offsetEnd": "0px",
                        "paddingTop": "20px",
                        "paddingBottom": "28px",
                    },
                ],
                "paddingAll": "0px",
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "教學", "text": "教學"},
                        "position": "relative",
                        "height": "sm",
                        "color": "#E5E3DF",
                    }
                ],
                "backgroundColor": "#666666",
                "paddingAll": "md",
            },
        }
        message = FlexSendMessage(alt_text="歡迎使用 Eatender！", contents=contents)
        return message

    def tutorial(self):
        contents = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "image",
                        "aspectMode": "cover",
                        "size": "full",
                        "gravity": "top",
                        "margin": "none",
                        "position": "relative",
                        "aspectRatio": "2:3",
                        "url": "https://i.imgur.com/RFqeCz2.jpg",
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "今晚，你或許會想先來點...",
                                        "size": "lg",
                                        "weight": "bold",
                                        "margin": "5px",
                                        "color": "#ffffff",
                                        "wrap": true,
                                    },
                                    {
                                        "type": "text",
                                        "text": "「使．用．教．學！」",
                                        "color": "#0E9721",
                                        "weight": "bold",
                                        "size": "lg",
                                    },
                                ],
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "icon",
                                        "url": "https://i.imgur.com/UQL7M2P.png",
                                        "size": "md",
                                    },
                                    {
                                        "type": "text",
                                        "text": "首先，設定您要用餐的地點",
                                        "margin": "5px",
                                        "size": "md",
                                        "weight": "bold",
                                    },
                                ],
                                "margin": "sm",
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "icon",
                                        "size": "md",
                                        "url": "https://i.imgur.com/49UpMsr.png",
                                    },
                                    {
                                        "type": "text",
                                        "text": "將喜歡的餐廳加入投票箱",
                                        "weight": "bold",
                                        "margin": "5px",
                                        "size": "md",
                                    },
                                ],
                                "margin": "sm",
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "icon",
                                        "url": "https://i.imgur.com/lNtabPe.png",
                                        "size": "md",
                                    },
                                    {
                                        "type": "text",
                                        "text": "點選投票 跟朋友決定最愛的餐廳",
                                        "size": "md",
                                        "margin": "5px",
                                        "weight": "bold",
                                    },
                                ],
                                "margin": "sm",
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "icon",
                                        "url": "https://i.imgur.com/247HjzP.png",
                                        "size": "md",
                                    },
                                    {
                                        "type": "text",
                                        "text": "導航至目的地，Let's dig in！",
                                        "size": "md",
                                        "margin": "5px",
                                        "weight": "bold",
                                        "color": "#EF4B26",
                                    },
                                ],
                                "margin": "sm",
                            },
                        ],
                        "backgroundColor": "#EBA909cc",
                        "position": "absolute",
                        "offsetStart": "0px",
                        "offsetEnd": "0px",
                        "offsetBottom": "250px",
                        "paddingAll": "20px",
                        "paddingTop": "100px",
                    },
                ],
                "paddingAll": "0px",
            },
        }
        message = FlexSendMessage(alt_text="使用教學", contents=contents)
        return message

    def show_vote_pull(self, restaurants):
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
            open_now = find_operating_status(
                data=each["operating_time"]["weekday_text"]
            )

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
                lat=lat,
                lng=lng,
            )
            show_list.append(card)
        contents = {
            "type": "carousel",
            "contents": show_list,
        }
        message = FlexSendMessage(alt_text="投票池列表", contents=contents)
        return message

    def show_favorite(self, restaurants):
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
            open_now = find_operating_status(
                data=each["operating_time"]["weekday_text"]
            )

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

    def show_restaurant(self, restaurants, keyword, next_page):
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
                user_lat=self.user_lat,
                user_lng=self.user_lng,
                keyword=keyword,
                next_page=next_page,
            )
            contents["contents"].append(more)
        message = FlexSendMessage(alt_text="餐廳推薦列表", contents=contents)
        return message

    def error(self):
        contents = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://i.imgur.com/c8RJZCY.png",
                "size": "full",
                "aspectRatio": "5:3",
                "aspectMode": "cover",
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "很抱歉！",
                        "weight": "bold",
                        "size": "xl",
                        "color": "#FF0000",
                        "align": "center",
                    },
                    {
                        "type": "text",
                        "text": "發生了些意料之外的錯誤，如果持續無法解決請聯繫客服！",
                        "wrap": true,
                    },
                ],
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "none",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "聯繫客服",
                                    "uri": "https://lin.ee/DsogwtP",
                                },
                                "color": "#000000",
                            }
                        ],
                        "backgroundColor": "#fdbe29",
                        "cornerRadius": "100px",
                        "margin": "none",
                        "alignItems": "center",
                        "justifyContent": "space-evenly",
                        "position": "relative",
                        "width": "200px",
                        "height": "50px",
                        "offsetStart": "40px",
                    }
                ],
            },
        }
        message = FlexSendMessage(alt_text="發生錯誤！", contents=contents)
        return message

    def share_vote(self, pull_id):
        contents = {
            "type": "carousel",
            "contents": [
                {
                    "type": "bubble",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "image",
                                        "url": "https://i.ibb.co/y09hjt2/LOGO5.png",
                                        "size": "full",
                                        "aspectMode": "cover",
                                        "aspectRatio": "20:12",
                                        "position": "relative",
                                    }
                                ],
                                "cornerRadius": "100px",
                            }
                        ],
                        "paddingAll": "0px",
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "餐廳選項建立完成",
                                        "size": "lg",
                                        "weight": "bold",
                                        "style": "normal",
                                        "wrap": true,
                                        "align": "center",
                                    }
                                ],
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "Step1. 左滑右滑來挑選餐廳",
                                                "color": "#666666",
                                                "size": "sm",
                                                "flex": 2,
                                            }
                                        ],
                                        "offsetTop": "sm",
                                        "borderWidth": "bold",
                                        "spacing": "sm",
                                        "flex": 2,
                                        "offsetBottom": "lg",
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "Step2. 選擇聚餐時間",
                                                "flex": 2,
                                                "size": "sm",
                                                "color": "#666666",
                                                "contents": [],
                                            }
                                        ],
                                        "borderWidth": "bold",
                                        "spacing": "sm",
                                        "offsetBottom": "lg",
                                        "offsetTop": "sm",
                                        "position": "relative",
                                        "flex": 2,
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "Step3. 投票完成，等待投票結果",
                                                "flex": 2,
                                                "size": "sm",
                                                "color": "#666666",
                                                "contents": [],
                                            }
                                        ],
                                        "borderWidth": "bold",
                                        "spacing": "sm",
                                        "offsetBottom": "lg",
                                        "offsetTop": "sm",
                                        "position": "relative",
                                        "flex": 2,
                                    },
                                ],
                                "spacing": "sm",
                            },
                        ],
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "uri",
                                            "label": "開始投票",
                                            "uri": f"https://liff.line.me/1655422218-8n1PlOw1?id={pull_id}",
                                        },
                                        "color": "#000000",
                                    }
                                ],
                                "backgroundColor": "#fdbe29",
                                "cornerRadius": "100px",
                                "margin": "none",
                                "alignItems": "center",
                                "justifyContent": "space-evenly",
                                "position": "relative",
                                "width": "200px",
                                "height": "50px",
                                "offsetStart": "40px",
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "uri",
                                            "label": "分享投票",
                                            "uri": f"https://liff.line.me/1655422218-O3KRZNpK?id={pull_id}",
                                        },
                                        "color": "#000000",
                                    }
                                ],
                                "backgroundColor": "#fdbe29",
                                "cornerRadius": "100px",
                                "margin": "lg",
                                "alignItems": "center",
                                "justifyContent": "space-evenly",
                                "position": "relative",
                                "width": "200px",
                                "height": "50px",
                                "offsetStart": "40px",
                            },
                        ],
                    },
                }
            ],
        }
        message = FlexSendMessage(alt_text="投票創建成功！", contents=contents)
        return message

    def liff_share(self, pull_id):
        contents = {
            "type": "carousel",
            "contents": [
                {
                    "type": "bubble",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "image",
                                        "url": "https://i.ibb.co/y09hjt2/LOGO5.png",
                                        "size": "full",
                                        "aspectMode": "cover",
                                        "aspectRatio": "20:12",
                                        "position": "relative",
                                    }
                                ],
                                "cornerRadius": "100px",
                            }
                        ],
                        "paddingAll": "0px",
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "餐廳選項建立完成",
                                        "size": "lg",
                                        "weight": "bold",
                                        "style": "normal",
                                        "wrap": true,
                                        "align": "center",
                                    }
                                ],
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "Step1. 左滑右滑來挑選餐廳",
                                                "color": "#666666",
                                                "size": "sm",
                                                "flex": 2,
                                            }
                                        ],
                                        "offsetTop": "sm",
                                        "borderWidth": "bold",
                                        "spacing": "sm",
                                        "flex": 2,
                                        "offsetBottom": "lg",
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "Step2. 選擇聚餐時間",
                                                "flex": 2,
                                                "size": "sm",
                                                "color": "#666666",
                                                "contents": [],
                                            }
                                        ],
                                        "borderWidth": "bold",
                                        "spacing": "sm",
                                        "offsetBottom": "lg",
                                        "offsetTop": "sm",
                                        "position": "relative",
                                        "flex": 2,
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "Step3. 投票完成，等待投票結果",
                                                "flex": 2,
                                                "size": "sm",
                                                "color": "#666666",
                                                "contents": [],
                                            }
                                        ],
                                        "borderWidth": "bold",
                                        "spacing": "sm",
                                        "offsetBottom": "lg",
                                        "offsetTop": "sm",
                                        "position": "relative",
                                        "flex": 2,
                                    },
                                ],
                                "spacing": "sm",
                            },
                        ],
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "none",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "uri",
                                            "label": "開始投票",
                                            "uri": f"https://liff.line.me/1655422218-8n1PlOw1?id={pull_id}",
                                        },
                                        "color": "#000000",
                                    }
                                ],
                                "backgroundColor": "#fdbe29",
                                "cornerRadius": "100px",
                                "margin": "none",
                                "alignItems": "center",
                                "justifyContent": "space-evenly",
                                "position": "relative",
                                "width": "200px",
                                "height": "50px",
                                "offsetStart": "40px",
                            }
                        ],
                    },
                }
            ],
        }
        return contents


def find_operating_status(data):
    now = datetime.now()
    weekday = now.weekday()
    time = now.strftime("%H:%M")

    today_open = data[weekday].split(",")
    for each in today_open:
        if "休息" in each:
            return False
        if "24 小時營業" in each:
            return True
        temp = re.findall(r"\d{1,2}\:\d{1,2}", each)
        start = datetime.strptime(f"{temp[0]}:{str(weekday)}", "%H:%M:%d")
        current = datetime.strptime(f"{time}:{str(weekday)}", "%H:%M:%d")
        if int(temp[0][0:2]) <= int(temp[1][0:2]):
            end = datetime.strptime(f"{temp[1]}:{str(weekday)}", "%H:%M:%d")
        else:
            end = datetime.strptime(f"{temp[1]}:{str(weekday + 1)}", "%H:%M:%d")

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
):
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

    if price == 0:
        price = "N/A"
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
    card = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "image",
                            "url": photo_url,
                            "size": "full",
                            "aspectMode": "cover",
                            "aspectRatio": "20:13",
                            "position": "relative",
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [operate_status],
                            "position": "absolute",
                            "flex": 0,
                            "width": "55px",
                            "height": "25px",
                            "backgroundColor": operate_color,
                            "cornerRadius": "100px",
                            "offsetTop": "18px",
                            "offsetStart": "18px",
                            "paddingAll": "2px",
                            "paddingStart": "4px",
                            "paddingEnd": "4px",
                        },
                    ],
                }
            ],
            "paddingAll": "0px",
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                        {
                            "type": "text",
                            "text": restaurant_name,
                            "size": "xl",
                            "weight": "bold",
                            "style": "normal",
                            "flex": 0,
                            "wrap": true,
                            "maxLines": 1,
                        }
                    ],
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "margin": "md",
                    "contents": star_list
                    + [
                        {
                            "type": "text",
                            "text": str(rating),
                            "size": "sm",
                            "color": "#999999",
                            "margin": "sm",
                            "flex": 0,
                        },
                    ],
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"${price}",
                            "size": "sm",
                            "color": "#999999",
                            "flex": 0,
                        },
                        {
                            "type": "text",
                            "text": "餐廳網站",
                            "action": {
                                "type": "uri",
                                "label": "action",
                                "uri": website,
                            },
                            "margin": "md",
                            "size": "sm",
                            "color": "#999999",
                            "decoration": "underline",
                            "flex": 0,
                        },
                        {
                            "type": "text",
                            "text": "愛食記",
                            "action": {
                                "type": "uri",
                                "label": "action",
                                "uri": ifoodie_url,
                            },
                            "flex": 0,
                            "margin": "md",
                            "size": "sm",
                            "color": "#999999",
                            "decoration": "underline",
                        },
                    ],
                    "offsetTop": "md",
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                        {
                            "type": "text",
                            "text": "評論",
                            "size": "sm",
                            "color": "#999999",
                            "flex": 0,
                        }
                    ]
                    + comments,
                    "offsetTop": "md",
                    "margin": "lg",
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "地點",
                                    "color": "#666666",
                                    "size": "sm",
                                    "flex": 2,
                                },
                                {
                                    "type": "text",
                                    "text": address,
                                    "color": "#666666",
                                    "size": "sm",
                                    "wrap": true,
                                    "flex": 6,
                                },
                            ],
                            "offsetTop": "lg",
                            "borderWidth": "bold",
                            "spacing": "sm",
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "電話",
                                    "flex": 2,
                                    "size": "sm",
                                    "color": "#666666",
                                    "contents": [],
                                },
                                {
                                    "type": "text",
                                    "flex": 6,
                                    "text": phone_number,
                                    "size": "sm",
                                    "color": "#666666",
                                    "wrap": true,
                                },
                            ],
                            "borderWidth": "bold",
                            "spacing": "sm",
                            "offsetBottom": "lg",
                            "offsetTop": "sm",
                            "position": "relative",
                        },
                    ],
                    "spacing": "sm",
                    "margin": "lg",
                },
            ],
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "none",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "uri",
                                "label": "前往",
                                "uri": f"https://www.google.com/maps/search/?api=1&query={lat},{lng}&travelmode=walking",
                            },
                            "offsetBottom": "md",
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "收藏",
                                "data": f"favorite_||_{place_id}",
                            },
                            "offsetBottom": "md",
                        },
                    ],
                    "spacing": "none",
                    "margin": "none",
                    "height": "40px",
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "加入投票",
                                "data": f"vote_||_{place_id}",
                            },
                            "color": "#000000",
                        }
                    ],
                    "backgroundColor": "#fdbe29",
                    "cornerRadius": "100px",
                    "margin": "none",
                    "alignItems": "center",
                    "justifyContent": "space-evenly",
                    "position": "relative",
                    "width": "200px",
                    "height": "50px",
                    "offsetStart": "40px",
                },
            ],
        },
    }
    return card


def show_more(user_lat, user_lng, keyword, next_page):
    card = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "image",
                    "url": "https://img.onl/qZkjv",
                    "size": "full",
                    "offsetTop": "40px",
                    "aspectMode": "fit",
                    "position": "relative",
                },
                {
                    "type": "text",
                    "text": "還想看更多餐廳嗎?",
                    "style": "normal",
                    "weight": "bold",
                    "offsetStart": "65px",
                    "size": "md",
                    "offsetTop": "35px",
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "查看更多",
                                "data": f"more_||_{user_lat},{user_lng}_||_{keyword}_||_{next_page}",
                            },
                            "position": "relative",
                            "color": "#296ae8",
                        }
                    ],
                    "width": "200px",
                    "backgroundColor": "#fdbe29",
                    "height": "50px",
                    "cornerRadius": "100px",
                    "justifyContent": "center",
                    "alignItems": "center",
                    "position": "relative",
                    "offsetTop": "45px",
                    "offsetStart": "30px",
                },
            ],
        },
    }
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
    lat: float,
    lng: float,
):
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

    if price == 0:
        price = "N/A"
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
    card = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "image",
                            "url": photo_url,
                            "size": "full",
                            "aspectMode": "cover",
                            "aspectRatio": "20:13",
                            "position": "relative",
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [operate_status],
                            "position": "absolute",
                            "flex": 0,
                            "width": "55px",
                            "height": "25px",
                            "backgroundColor": operate_color,
                            "cornerRadius": "100px",
                            "offsetTop": "18px",
                            "offsetStart": "18px",
                            "paddingAll": "2px",
                            "paddingStart": "4px",
                            "paddingEnd": "4px",
                        },
                    ],
                }
            ],
            "paddingAll": "0px",
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                        {
                            "type": "text",
                            "text": restaurant_name,
                            "size": "xl",
                            "weight": "bold",
                            "style": "normal",
                            "flex": 0,
                            "wrap": true,
                            "maxLines": 1,
                        }
                    ],
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "margin": "md",
                    "contents": star_list
                    + [
                        {
                            "type": "text",
                            "text": str(rating),
                            "size": "sm",
                            "color": "#999999",
                            "margin": "sm",
                            "flex": 0,
                        },
                    ],
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"${price}",
                            "size": "sm",
                            "color": "#999999",
                            "flex": 0,
                        },
                        {
                            "type": "text",
                            "text": "餐廳網站",
                            "action": {
                                "type": "uri",
                                "label": "action",
                                "uri": website,
                            },
                            "margin": "md",
                            "size": "sm",
                            "color": "#999999",
                            "decoration": "underline",
                            "flex": 0,
                        },
                        {
                            "type": "text",
                            "text": "愛食記",
                            "action": {
                                "type": "uri",
                                "label": "action",
                                "uri": ifoodie_url,
                            },
                            "flex": 0,
                            "margin": "md",
                            "size": "sm",
                            "color": "#999999",
                            "decoration": "underline",
                        },
                    ],
                    "offsetTop": "md",
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                        {
                            "type": "text",
                            "text": "評論",
                            "size": "sm",
                            "color": "#999999",
                            "flex": 0,
                        }
                    ]
                    + comments,
                    "offsetTop": "md",
                    "margin": "lg",
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "地點",
                                    "color": "#666666",
                                    "size": "sm",
                                    "flex": 2,
                                },
                                {
                                    "type": "text",
                                    "text": address,
                                    "color": "#666666",
                                    "size": "sm",
                                    "wrap": true,
                                    "flex": 6,
                                },
                            ],
                            "offsetTop": "lg",
                            "borderWidth": "bold",
                            "spacing": "sm",
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "電話",
                                    "flex": 2,
                                    "size": "sm",
                                    "color": "#666666",
                                    "contents": [],
                                },
                                {
                                    "type": "text",
                                    "flex": 6,
                                    "text": phone_number,
                                    "size": "sm",
                                    "color": "#666666",
                                    "wrap": true,
                                },
                            ],
                            "borderWidth": "bold",
                            "spacing": "sm",
                            "offsetBottom": "lg",
                            "offsetTop": "sm",
                            "position": "relative",
                        },
                    ],
                    "spacing": "sm",
                    "margin": "lg",
                },
            ],
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "none",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "移除餐廳",
                                "data": f"remove_||_{place_id}",
                            },
                            "color": "#000000",
                        }
                    ],
                    "backgroundColor": "#fdbe29",
                    "cornerRadius": "100px",
                    "margin": "none",
                    "alignItems": "center",
                    "justifyContent": "space-evenly",
                    "position": "relative",
                    "width": "200px",
                    "height": "50px",
                    "offsetStart": "40px",
                }
            ],
        },
    }

    return card
