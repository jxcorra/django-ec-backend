from typing import Dict

from django.db.models import Manager, QuerySet


class ModelsManager(Manager):
    def order_by_query(self, query: str) -> QuerySet:
        return

    def filter_dynamic(self, query: Dict) -> QuerySet:
        return self.filter(**query)
