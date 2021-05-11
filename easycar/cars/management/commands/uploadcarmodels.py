import concurrent.futures
import json.decoder
import logging
import sys
import typing

import requests
from django.core.management import BaseCommand, CommandParser

from cars.models import Model, Make

logger = logging.getLogger(__name__)
logger.addHandler(
    logging.StreamHandler(sys.stdout)
)

MAKES_API_URL = 'https://vpic.nhtsa.dot.gov/api/vehicles/GetMakesForVehicleType/car?format=json'
MODELS_PER_MAKE_API_URL = 'https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/{make}?format=json'
DEFAULT_MAX_WORKERS = 1


class Command(BaseCommand):
    help = 'Creates all makes and models in database provided by `vpic.nhtsa.dot.gov` api'

    def handle(self, *args, **options):
        with_reset = options.get('with_reset', False)
        max_workers = options.get('max_workers', DEFAULT_MAX_WORKERS)

        if with_reset:
            self.__delete_models()
            self.__delete_makes()
            logger.info('Successfully removed all car models and makes.')

        make_results = requests.get(MAKES_API_URL).json()['Results']

        makes = []
        for make_result in make_results:
            makes.append(self.__create_make_from_json(make_result))
        Make.objects.bulk_create(makes)

        makes_count = Make.objects.count()
        logger.info(f'{makes_count} makes added.')

        # use concurrent here
        models = []
        futures = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
            for make in Make.objects.all():
                futures.append(pool.submit(self.__request_make_models, make))

            for ready_future in concurrent.futures.as_completed(futures):
                try:
                    model_results = ready_future.result()
                except json.decoder.JSONDecodeError:
                    # Some responses may contain invalid json data so just skip them
                    continue

                for model_result in model_results:
                    models.append(self.__create_model_from_json(make, model_result))
                Model.objects.bulk_create(models)

                models_count = Model.objects.filter(make=make).count()
                logger.info(f'{models_count} models added for {make.name} make.')

    def __request_make_models(self, make: Make) -> typing.List:
        return requests.get(MODELS_PER_MAKE_API_URL.format(make=make.name)).json()['Results']

    def __delete_models(self):
        Model.objects.all().delete()

    def __delete_makes(self):
        Make.objects.all().delete()

    def __create_make_from_json(self, serialized_make: typing.Dict) -> Make:
        return Make(name=serialized_make['MakeName'])

    def __create_model_from_json(self, make: Make, serialized_model: typing.Dict) -> Model:
        return Model(name=serialized_model['Model_Name'][:64], make=make)

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '--with-reset',
            action='store_const',
            const=True,
            help='Removes all existing makes and models first'
        )

        parser.add_argument(
            '--max-workers',
            type=int,
            help='Max concurrent workers for car models fetching'
        )
