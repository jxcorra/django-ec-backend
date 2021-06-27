import typing

import requests

from cars.models import Make

MAKES_API_URL = 'https://vpic.nhtsa.dot.gov/api/vehicles/GetMakesForVehicleType/car?format=json'
MODELS_PER_MAKE_API_URL = 'https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/{make}?format=json'


def get_makers() -> typing.List:
    return requests.get(MAKES_API_URL).json()['Results']


def get_maker_models(make: Make) -> typing.List:
    return requests.get(MODELS_PER_MAKE_API_URL.format(make=make.name)).json()['Results']
