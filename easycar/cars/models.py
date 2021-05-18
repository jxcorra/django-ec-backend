from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.db import models

# Create your models here.
from cars.managers import CarManager
from core.models import TimestampedModel, SafeDeleteModel


class Make(TimestampedModel, SafeDeleteModel, models.Model):
    name = models.CharField(max_length=64, help_text='Car model make', unique=True)

    def __str__(self):
        return f'Make name={self.name}'


class Model(TimestampedModel, SafeDeleteModel, models.Model):
    name = models.CharField(max_length=128, help_text='Car model', unique=True)
    make = models.ForeignKey(
        to=Make, on_delete=models.CASCADE, related_name='models',
    )

    def __str__(self):
        return f'Model name={self.name} make={self.make.name}'


class Car(TimestampedModel, SafeDeleteModel, models.Model):
    owner = models.ForeignKey(
        to='auth.User',  # default django user model used (auth using username and password)
        on_delete=models.CASCADE, related_name='cars', help_text='Car owner'
    )
    model = models.OneToOneField(to=Model, on_delete=models.SET_NULL, help_text='Car model', null=True, blank=True)
    vin = models.CharField(max_length=64, help_text='Car vin number', null=True, blank=True)
    year = models.IntegerField(help_text='Car released year')
    image = models.FileField(storage=default_storage, max_length=2 * 1024, null=True, blank=True)

    objects = CarManager()

    def __str__(self):
        return f'Car owner={self.owner.username} model={self.model.name} year={self.year}'
