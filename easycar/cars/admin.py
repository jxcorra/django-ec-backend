from django.contrib import admin

# Register your models here.
from cars.models import Make, Model


@admin.register(Make)
class CarMakeAdmin(admin.ModelAdmin):
    fields = ('name',)


@admin.register(Model)
class CarModelAdmin(admin.ModelAdmin):
    fields = ('name', 'make',)
    list_filter = ('make__name',)
