import re
from datetime import datetime, timedelta

from linebot.models import FlexSendMessage

from config import console

true = True


class Template:
    def __init__(self, user_lat=0, user_lng=0):
        self.user_lat = user_lat
        self.user_lng = user_lng

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


def find_operating_status(data):
    now = datetime.now()
    today_date = now.strftime("%Y:%m:%d")
    time = now.strftime("%H:%M")

    today_open = data[now.weekday()].split(",")
    for each in today_open:
        if "休息" in each:
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
                                "data": f"favorite_{place_id}",
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
                                "data": f"vote_{place_id}",
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
                                "data": f"more_{user_lat},{user_lng}_{keyword}_{next_page}",
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
                                "data": f"remove_{place_id}",
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
