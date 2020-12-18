import jieba

stop_words = []
with open("food/stop_words.txt", "r", encoding="UTF-8") as file:
    for data in file.readlines():
        data = data.strip()
        stop_words.append(data)


class Restaurant:
    def __init__(
        self,
        place_id: str,
        name: str,
        photo_url: str,
        open_now: bool,
        operating_time: dict,
        location: dict,
        address: str,
        rating: float,
        website: str,
        google_url: str,
        price: int = 0,
        phone_number: str = "無",
        reviews: list = [""],
        ifoodie_url: str = "https://ifoodie.tw/",
    ):
        self.place_id = place_id
        self.name = name
        self.photo_url = photo_url
        self.open_now = open_now
        self.operating_time = operating_time
        self.next_open_time = ""
        self.location = location
        self.address = address
        self.rating = rating
        self.website = website
        self.google_url = google_url
        self.price = price
        self.phone_number = phone_number
        self.reviews = reviews
        self.keywords = self.find_keywords(name=name, reviews=reviews)
        self.ifoodie_url = ifoodie_url

    def find_keywords(self, name, reviews):
        keyword_data = {}
        keywords = []
        for review in reviews:
            segments = jieba.cut(review, use_paddle=True)
            remainder_words = list(
                filter(
                    lambda a: a not in stop_words
                    and a is not name
                    and a != "\n"
                    and a.replace(" ", "") != "",
                    segments,
                )
            )
            for word in remainder_words:
                if word in keyword_data:
                    keyword_data[word] += 1
                else:
                    keyword_data[word] = 1
        most_frequent = sorted(keyword_data.items(), key=lambda x: -x[1])
        for each in most_frequent[:3]:
            keywords.append(each[0])
        return keywords

    def real_keyword(self):
        pass
