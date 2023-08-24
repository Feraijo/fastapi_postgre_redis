from fastapi import APIRouter
from docs_app.controllers.city_weather_controller import \
    CityWeatherController
from docs_app.models.model import CityWeather
from docs_app.core.config import settings

router = APIRouter()

base_url = f'http://{settings.PRJ_HOST}/docs'


@router.get("/")
async def usage():
    return [{'Endpoints': {
            'Get document: ': base_url,
            'Post new document: ': base_url + '/new',
            'Update existing document: ': base_url + '/put/<id>',
            'Delete existing document: ': base_url + '/delete/<id>',
        }
    }]


@router.get("/docs")
async def get_user_documents(city_name: str) -> CityWeather:
    return await CityWeatherController.create(city_name)
