from linebot.models import FlexSendMessage

true = True


class Template:
    def show_nearby_restaurant(self, restaurants):
        show_list = []
        for each in restaurants:
            restaurant_name = each.name
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
            card = restaurant_carousel(
                restaurant_name=restaurant_name,
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
        message = FlexSendMessage(alt_text="餐廳推薦列表", contents=contents)
        return message


def restaurant_carousel(
    restaurant_name: str,
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

    # TODO: 確切時間
    if open_now:
        operate_status = {
            "type": "text",
            "text": "營業中",
            "margin": "md",
            "size": "sm",
            "color": "#5ba709",
        }
    else:
        operate_status = {
            "type": "text",
            "text": "尚未營業",
            "margin": "md",
            "size": "sm",
            "color": "#ff0000",
        }
    card = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": photo_url,
            "position": "relative",
            "gravity": "top",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "offsetTop": "md",
            "offsetStart": "none",
            "offsetEnd": "none",
            "offsetBottom": "none",
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
                        },
                        operate_status,
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
                            "text": "4.0",
                            "size": "sm",
                            "color": "#999999",
                            "margin": "sm",
                            "flex": 0,
                        },
                        {
                            "type": "text",
                            # TODO: 關鍵詞列表
                            "text": "關鍵字",
                            "margin": "md",
                            "size": "sm",
                            "color": "#999999",
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
                    "offsetTop": "sm",
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
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
                            "offsetTop": "md",
                        },
                    ],
                },
            ],
        },
        "footer": {
            "type": "box",
            "layout": "horizontal",
            "spacing": "none",
            "contents": [
                {
                    "type": "button",
                    "action": {"type": "message", "label": "喜歡", "text": "要不要考慮前往用餐呢~"},
                    "color": "#3F67C6",
                },
                {
                    "type": "button",
                    "action": {
                        "type": "uri",
                        "label": "前往",
                        "uri": f"https://www.google.com/maps/search/?api=1&query={lat},{lng}&travelmode=walking",
                    },
                    "color": "#000000",
                },
                {
                    "type": "button",
                    "action": {"type": "message", "label": "收藏", "text": "已經加入你的收藏了~"},
                    "color": "#3F67C6",
                },
            ],
            "backgroundColor": "#FFFACD",
            "offsetTop": "sm",
            "paddingAll": "md",
        },
    }
    return card
