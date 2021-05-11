from django.db import models

# Create your models here.


class Make(models.Model):
    name = models.CharField(max_length=64, help_text='Car model make')


class Model(models.Model):
    name = models.CharField(max_length=64, help_text='Car model')
    make = models.ForeignKey(
        to=Make, on_delete=models.CASCADE, related_name='models',
    )
