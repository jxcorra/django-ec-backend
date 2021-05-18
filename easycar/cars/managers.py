from typing import Dict

from django.db.models import Manager, QuerySet
from django.utils import timezone


class ModelsManager(Manager):
    def filter_dynamic(self, query: Dict) -> QuerySet:
        return self.filter(**query)


class CarManager(Manager):
    def fresh_cars(self):
        return self.filter(year__gte=timezone.now().year - 10)
