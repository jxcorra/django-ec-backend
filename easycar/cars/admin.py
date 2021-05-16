from django.contrib import admin

# Register your models here.
from cars.models import Make, Model, Car


@admin.register(Make)
class CarMakeAdmin(admin.ModelAdmin):
    fields = ('name',)


@admin.register(Model)
class CarModelAdmin(admin.ModelAdmin):
    fields = ('name', 'make',)
    list_filter = ('make__name',)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    fields = ('owner', 'model', 'year', 'vin', 'image',)
    list_filter = ('owner', 'model', 'year',)