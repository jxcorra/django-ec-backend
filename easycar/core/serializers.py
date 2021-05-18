from rest_framework import serializers


class TimestampedSerializer(serializers.Serializer):
    created = serializers.DateTimeField(source='date_created')  # rename field
    updated = serializers.DateTimeField(source='date_updated')
    removed = serializers.DateTimeField(source='date_removed')
    is_removed = serializers.SerializerMethodField(read_only=True)

    def get_is_removed(self) -> bool:
        return self.removed is not None
