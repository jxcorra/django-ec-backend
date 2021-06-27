import logging
from typing import List

import core.carinfoapi
from celery import shared_task

from cars.models import Make, Model


logger = logging.getLogger()


@shared_task(
    name='cars.refresh_makers',
    ignore_result=True, queue='makers',
    soft_time_limit=60
)
def bulk_refresh_makers_list() -> None:
    logger.info('Starting makers refresh')

    makers_to_create: List[Make] = []

    existing_maker_names = [maker['name'] for maker in Make.objects.all().values('name')]
    for raw_maker_name in map(lambda maker: maker['MakeName'], core.carinfoapi.get_makers()):
        if raw_maker_name in existing_maker_names:
            continue

        makers_to_create.append(Make(name=raw_maker_name))

    Make.objects.bulk_create(makers_to_create)


@shared_task(
    name='cars.run_refresh_models',
    ignore_result=True, queue='models',
    soft_time_limit=60
)
def run_refresh_makers_models():
    logger.info('Starting models refresh')

    for maker in Make.objects.all():
        refresh_maker_models_list.delay(maker.name)


@shared_task(
    name='cars.refresh_models',
    ignore_result=True, queue='models',
    max_retries=5, soft_time_limit=60
)
def refresh_maker_models_list(maker_name: str) -> None:
    make = Make.objects.get(name=maker_name)
    models_to_create: List[Model] = []

    existing_models_names = [model['name'] for model in Model.objects.filter(make=make).values('name')]
    for raw_model_name in map(lambda model: model['Model_Name'][:64], core.carinfoapi.get_maker_models(make)):
        if raw_model_name in existing_models_names:
            continue

        models_to_create.append(Model(name=raw_model_name, make=make))

    Model.objects.bulk_create(models_to_create)
