from .google_maps.info import GM_Restaurant
from .ifoodie.ifoodie import Ifoodie


class Restaurant_data:
    def __init__(self, latitude, longitude, keyword):
        self.restaurants = []
        self.latitude = latitude
        self.longitude = longitude
        self.keyword = keyword

    def get_info(self):
        self.get_google_maps_data()
        self.get_ifoodie_data()

    def get_google_maps_data(self):
        restaurants = GM_Restaurant()
        restaurants.fetch_data(
            latitude=self.latitude, longitude=self.longitude, keyword=self.keyword
        )
        self.restaurants = restaurants.restaurants

    def get_ifoodie_data(self):
        for restaurant in self.restaurants:
            data = Ifoodie(
                restaurant_name=restaurant.name, restaurant_address=restaurant.address
            )
            # TODO: Continue
