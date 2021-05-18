from django.urls import re_path, path

from cars.views import (
    list_make_view,
    details_make_view,
    list_model_view,
    details_model_view,
    list_car_view,
    details_car_view,
)

urlpatterns = [
    path('makes/', list_make_view, name='makes-list'),
    re_path(r'/makes/(?P<make_id>\d+)', details_make_view, name='make-details'),
    path('models/', list_model_view, name='models-list'),
    re_path(r'/models/(?P<model_id>\d+)', details_model_view, name='model-details'),
    path('cars/', list_car_view, name='cars-list'),
    re_path(r'/cars/(?P<car_id>\d+)', details_car_view, name='car-details'),
]
