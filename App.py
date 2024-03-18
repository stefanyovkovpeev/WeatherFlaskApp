from random import random
import json
import gzip
import random
import requests
from decouple import config


class App:

    def __init__(self):
        self.cities = ["New York", "Sofia", "London", "Tokyo", "Sydney"]
        self.weather_data = {}
        self.get_weather(self.cities)


    def random_cities_generator(self):
        url = "http://bulk.openweathermap.org/sample/city.list.json.gz"

        response = requests.get(url)

        if response.status_code == 200:
            with open("city_data.json.gz", "wb") as f:
                f.write(response.content)

            with gzip.open("city_data.json.gz", "rb") as f:
                city_data = json.load(f)

            city_names = [city['name'] for city in city_data]

            random_cities = random.sample(city_names, 5)

        else:
            return "Unavailable"

        self.cities = random_cities

    def get_weather(self, cities):
        self.weather_data_fetched = {}

        base_url = "http://api.openweathermap.org/data/2.5/weather"
        for city in cities:
            params = {
                'q': city,
                'appid': config('YOUR_API_KEY'),
                'units': 'metric'
            }
            response = requests.get(base_url, params=params)
            data = response.json()

            conditions = data['weather'][0]['description']
            temp_current = round(data['main']['temp'])
            humidity = data['main']['humidity']

            self.weather_data_fetched[city] = {
                "name": city,
                'temp_current': temp_current,
                'humidity': humidity,
                'conditions': conditions,
            }

        self.temperatures = [self.weather_data_fetched[city]['temp_current'] for city in self.cities]
        self.coldest_city = self.cities[self.temperatures.index(min(self.temperatures))]
        self.average_temperature = sum(self.temperatures) / len(self.temperatures)

        self.weather_data_fetched["Average"] = {
            "Average_temp":self.average_temperature,
            "Coldest_city":self.coldest_city,
        }


        self.weather_data = self.weather_data_fetched

    def search_city(self, city):
        try:
            base_url = "http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': city,
                'appid': config('YOUR_API_KEY'),
                'units': 'metric'
            }
            response = requests.get(base_url, params=params)
            data = response.json()

            conditions = data['weather'][0]['description']
            temp_current = round(data['main']['temp'])
            humidity = data['main']['humidity']

            city = city.capitalize()
            data_list = [temp_current, humidity, conditions, city]

            return data_list

        except:
            return None


    def get_cities(self):
        return self.cities

    def get_weather_data(self):
        return self.weather_data