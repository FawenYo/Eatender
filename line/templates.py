from linebot.models import FlexSendMessage

true = True


class Template:
    def show_nearby_restaurant(self, restaurants):
        show_list = []
        for each in restaurants:
            restaurant_name = each.name
            photo_url = each.photo_url
            rating = each.rating
            price = each.price
            address = each.address
            operating_time = "測試"
            phone_number = each.phone_number
            lat = each.location["lat"]
            lng = each.location["lng"]
            card = restaurant_carousel(
                restaurant_name=restaurant_name,
                photo_url=photo_url,
                rating=rating,
                price=price,
                address=address,
                operating_time=operating_time,
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
    rating: float,
    price: int,
    address: str,
    operating_time: str,
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

    card = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": photo_url,
            "position": "relative",
            "gravity": "top",
            "size": "5xl",
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
                    "type": "text",
                    "text": restaurant_name,
                    "weight": "bold",
                    "size": "xl",
                    "margin": "md",
                    "style": "normal",
                    "decoration": "none",
                    "position": "relative",
                    "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": "https://nonamecurryntu.oddle.me/zh_TW",
                    },
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
                            "margin": "md",
                            "flex": 0,
                        },
                        {
                            "type": "text",
                            "text": f"${price}",
                            "margin": "md",
                            "size": "sm",
                            "flex": 0,
                            "color": "#999999",
                        },
                        {
                            "type": "text",
                            "text": "愛食記評論(測試)",
                            "flex": 0,
                            "margin": "md",
                            "size": "sm",
                            "color": "#999999",
                            "style": "normal",
                            "decoration": "underline",
                            "action": {
                                "type": "uri",
                                "label": "action",
                                "uri": "https://ifoodie.tw/restaurant/5ebff6ee2756dd19c9dac4f2-NoName%E5%92%96%E5%93%A9%E3%82%AB%E3%83%AC%E3%83%BC%E3%83%A9%E3%82%A4%E3%82%B9%E5%8F%B0%E5%A4%A7%E5%BA%97",
                            },
                        },
                    ],
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
                                    "color": "#aaaaaa",
                                    "size": "sm",
                                    "flex": 2,
                                },
                                {
                                    "type": "text",
                                    "text": address,
                                    "wrap": true,
                                    "color": "#666666",
                                    "size": "sm",
                                    "flex": 5,
                                },
                            ],
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "營業時間",
                                    "color": "#aaaaaa",
                                    "size": "sm",
                                    "flex": 2,
                                },
                                {
                                    "type": "text",
                                    "text": operating_time,
                                    "wrap": true,
                                    "color": "#666666",
                                    "size": "sm",
                                    "flex": 5,
                                },
                            ],
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
                                    "color": "#aaaaaa",
                                    "contents": [],
                                },
                                {
                                    "type": "text",
                                    "flex": 5,
                                    "text": phone_number,
                                    "size": "sm",
                                    "color": "#666666",
                                    "wrap": true,
                                },
                            ],
                        },
                    ],
                },
            ],
        },
        "footer": {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "action": {"type": "message", "label": "喜歡", "text": "要不要考慮前往用餐呢~"},
                    "offsetTop": "none",
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
            "flex": 0,
            "backgroundColor": "#FFFACD",
        },
    }
    return card
