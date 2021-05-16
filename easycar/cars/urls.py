from django.urls import re_path, path

from cars.views import list_make_view, create_make_view, list_model_view, list_car_view, car_details_view

urlpatterns = [
    path('makes/', list_make_view, name='makes-list'),
    path('makes-new/', create_make_view, name='makes-add'),
    re_path(r'^makes/(?P<make_id>\d+)/models/$', list_model_view, name='models-list'),
    re_path(r'^makes/(?P<make_id>\d+)/models/(?P<model_id>\d+)/cars$', list_car_view, name='model-cars-list'),
    re_path(r'^cars/(?P<car_id>\d+)$', car_details_view, name='car-details'),
]
