import datetime

from rest_framework import serializers

from core.models import SafeDeleteModel


class TimestampedSerializer(serializers.Serializer):
    created = serializers.DateTimeField(source='date_created')  # rename field
    updated = serializers.DateTimeField(source='date_updated')


class TimestampedWithRemovedSerializer(TimestampedSerializer):
    removed = serializers.DateTimeField(source='date_removed')
    is_removed = serializers.SerializerMethodField(read_only=True)

    def get_is_removed(self, obj: SafeDeleteModel) -> bool:
        return obj.date_removed is not None
