from rest_framework import serializers

from cars.models import Make, Model, Car
from core.serializers import TimestampedWithRemovedSerializer
from users.serializers import UserSerializer


class MakeSerializer(serializers.ModelSerializer):
    # An example with fields specified
    class Meta:
        model = Make
        fields = ('id', 'name', 'date_created', 'date_updated', 'date_removed',)
        read_only_fields = ('id',)


class ModelSerializer(TimestampedWithRemovedSerializer, serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'

    id = serializers.IntegerField(read_only=True)
    make = MakeSerializer()
    name = serializers.CharField()


class BaseCarSerializer(TimestampedWithRemovedSerializer, serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

    id = serializers.IntegerField(read_only=True)
    model = ModelSerializer()
    vin = serializers.CharField()
    year = serializers.IntegerField()


class CarWithOwnerSerializer(BaseCarSerializer):
    owner = UserSerializer()
