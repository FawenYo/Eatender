class Restaurant:
    def __init__(
        self,
        name: str,
        photo_url: str,
        open_now: bool,
        operating_time: dict,
        location: dict,
        address: str,
        rating: float,
        website: str,
        price: int = 0,
        phone_number: str = "無",
        reviews: list = [""],
        ifoodie_url: str = "https://ifoodie.tw/",
    ):
        self.name = name
        self.photo_url = photo_url
        self.open_now = open_now
        self.operating_time = operating_time
        self.next_open_time = ""
        self.location = location
        self.address = address
        self.rating = rating
        self.website = website
        self.price = price
        self.phone_number = phone_number
        self.keywords = []
        self.reviews = reviews
        self.ifoodie_url = ifoodie_url
        self.find_operating_time(operating_time=operating_time)
        self.find_keywords(reviews=reviews)

    def find_keywords(self, reviews):
        pass

    def find_operating_time(self, operating_time):
        pass
