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
        price: int = 0,
        phone_number: str = "無",
        reviews: list = [""],
    ):
        self.name = name
        self.photo_url = photo_url
        self.open_now = open_now
        self.operating_time = operating_time
        self.next_open_time = ""
        self.location = location
        self.address = address
        self.rating = rating
        self.price = price
        self.phone_number = phone_number
        self.keywords = []
        self.reviews = reviews
        self.find_operating_time(operating_time=operating_time)
        self.find_keywords(reviews=reviews)

    def find_keywords(self, reviews):
        pass

    def find_operating_time(self, operating_time):
        pass
