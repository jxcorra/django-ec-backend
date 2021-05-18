from django.db.models import Manager


class BaseFilteringManager(Manager):
    def not_deleted(self):
        return self.filter(date_removed__isnull=True)
