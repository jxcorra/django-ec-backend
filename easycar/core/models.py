from django.db import models

# Create your models here.
from django.utils import timezone


class TimestampedModel(models.Model):
    class Meta:
        abstract = True

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class SafeDeleteModel(models.Model):
    class Meta:
        abstract = True

    date_removed = models.DateTimeField(null=True, blank=True)

    def delete(self, *args, safe=True):
        if safe:
            self.date_removed = timezone.now()
            return self.save()

        return super(SafeDeleteModel, self).delete(*args)
