from rest_framework import serializers
from ride.models import Rides
from driver.models import Driver
from api.v1.driver.serializers import DriverListSerializer


class RidesListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rides
        fields = "__all__"


class RidesListWithAvailableDriversSerializer(serializers.ModelSerializer):
    available_drivers = serializers.SerializerMethodField()

    class Meta:
        model = Rides
        fields = (
            'rider',
            'available_drivers',
            'pickup_location',
            'dropoff_location',
            'current_location',
            'status',
            'created_at',
            'updated_at'
        )
    def get_available_drivers(self,instance):
        if instance.status == 'available' :
           drivers = Driver.objects.filter(location=instance.pickup_location,status='available')
           serializer_data = DriverListSerializer(drivers,many=True).data
           return serializer_data
        else:
            return []
        
        
        