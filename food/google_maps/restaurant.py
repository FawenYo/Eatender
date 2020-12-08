class Restaurant:
    def __init__(self):
        self.name: str = ""
        self.photo: str = ""
        self.open: bool = False
        self.location: dict = {"lat": 0.0, "lng": 0.0}
