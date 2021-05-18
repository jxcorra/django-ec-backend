from typing import Dict

from django.db.models import QuerySet
from django.utils import timezone

from core.managers import BaseFilteringManager


class MakeManager(BaseFilteringManager):
    pass


class ModelManager(BaseFilteringManager):
    def filter_dynamic(self, query: Dict) -> QuerySet:
        return self.filter(**query)


class CarManager(BaseFilteringManager):
    def fresh_cars(self):
        return self.filter(year__gte=timezone.now().year - 10)
