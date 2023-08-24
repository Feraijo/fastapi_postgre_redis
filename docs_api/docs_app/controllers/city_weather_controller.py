import asyncio

from docs_app.models.city_weather import CityWeather
from docs_app.utility.weather_randomizer import get_city_weather


class CityWeatherController():

    @classmethod
    async def create(cls, city_name):
        await asyncio.sleep(2)  # imitate api call
        return CityWeather(city_name=city_name, weather=get_city_weather(city_name))
