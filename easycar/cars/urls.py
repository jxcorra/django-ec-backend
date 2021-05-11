from django.conf.urls import url

from cars.views import list_make_view, create_make_view, list_model_view

urlpatterns = [
    url('^makes$', list_make_view, name='makes-list'),
    url('^makes-new$', create_make_view, name='makes-add'),
    url(r'^makes/(?P<make_id>\d+)/models$', list_model_view, name='models-list'),
]