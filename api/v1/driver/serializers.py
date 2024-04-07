from rest_framework import serializers
from driver.models import Driver


class DriverListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Driver
        fields = (
            'id',
            'username',
            'location',
            'status'
        )