# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from cars.models import Make, Model, Car
from cars.serializers import MakeSerializer, ModelSerializer, CarWithOwnerSerializer
from core.paginators import LargeResultsSetPagination, StandardResultsSetPagination


class MakeListView(generics.ListCreateAPIView):
    serializer_class = MakeSerializer
    queryset = Make.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    pagination_class = LargeResultsSetPagination


class MakeDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MakeSerializer
    queryset = Make.objects.not_deleted()


class ModelListView(generics.ListCreateAPIView):
    serializer_class = ModelSerializer
    queryset = Model.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['make__id']


class ModelDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ModelSerializer
    queryset = Model.objects.not_deleted()


class CarListView(generics.ListCreateAPIView):
    serializer_class = CarWithOwnerSerializer
    queryset = Car.objects.all()
    pagination_class = StandardResultsSetPagination


class CarDetailsView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'car_pk'
    serializer_class = CarWithOwnerSerializer
    queryset = Car.objects.not_deleted()

    def get_object(self):
        lookup_field_value = self.kwargs[self.lookup_field]
        return Car.objects.get(pk=lookup_field_value)


list_make_view = MakeListView.as_view()
details_make_view = MakeDetailsView.as_view()
list_model_view = ModelListView.as_view()
details_model_view = ModelDetailsView.as_view()
list_car_view = CarListView.as_view()
details_car_view = CarDetailsView.as_view()
