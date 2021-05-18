from rest_framework import serializers

from cars.models import Make, Model, Car
from core.serializers import TimestampedSerializer


class MakeSerializer(serializers.ModelSerializer):
    # An example with fields specified
    class Meta:
        model = Make
        fields = ('id', 'name', 'date_created', 'date_updated', 'date_removed',)


class ModelSerializer(TimestampedSerializer, serializers.ModelSerializer):
    class Meta:
        model = Model

    id = serializers.IntegerField()
    name = serializers.CharField()


class BaseCarSerializer(ModelSerializer):
    class Meta:
        model = Car

    model = serializers.PrimaryKeyRelatedField()
    vin = serializers.CharField()
    year = serializers.IntegerField()


class CarWithOwnerSerializer(BaseCarSerializer):
    owner = serializers.PrimaryKeyRelatedField()
