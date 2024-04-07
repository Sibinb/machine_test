from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from ride.models import Rides
from .serializers import RidesListSerializer, RidesListWithAvailableDriversSerializer


class RidesListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        rides = Rides.objects.all()
        serializer_data = RidesListSerializer(rides, many=True).data

        response_data = {
            "app_data": {
                "data": serializer_data
            },
            "StatusCode": 6000
        }

        return Response(response_data)


class CreateRideView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        rider = request.data.get('rider')
        pickup_location = request.data.get('pickup_location')
        dropoff_location = request.data.get('dropoff_location')

        if rider and pickup_location and dropoff_location:
            ride = Rides.objects.create(
                rider=rider, pickup_location=pickup_location, dropoff_location=dropoff_location,)
            ride_id = ride.id

            response_data = {
                "app_data": {
                    "data": {
                        "ride_id": ride_id
                    },
                },
                "message": "Ride Created",
                "StatusCode": 6000
            }

            return Response(response_data)
        else:
            response_data = {
                "app_data": {
                    "message": "Enter all details",
                    "StatusCode": 6001
                }
            }

            return Response(response_data)


class ListSingleRideView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        ride = Rides.objects.filter(id=id)
        if ride.exists():
            ride = ride[0]
            serializer_data = RidesListSerializer(ride, many=False).data

            response_data = {
                "app_data": {
                    "data": serializer_data
                },
                "StatusCode": 6000
            }

            return Response(response_data)
        else:
            response_data = {
                "app_data": {
                    "message": "ride not found"
                },
                "StatusCode": 6001
            }

            return Response(response_data)


class RideStatusUpdateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, id):
        ride = Rides.objects.filter(id=id)
        if ride.exists():
            ride = ride[0]
            status = request.data.get('status')
            if status:
                if (status == 'cancelled' or status == 'completed') and ride.driver:
                    ride.status = status
                    ride.driver.status = "available"
                    ride.driver.save()
                    ride.save()
                else:
                    ride.status = status
                    ride.save()
                response_data = {
                    "app_data": {
                        "message": "status updated"
                    },
                    "StatusCode": 6000
                }

                return Response(response_data)
            else:
                response_data = {
                    "app_data": {
                        "message": "Give a valid status"
                    },
                    "StatusCode": 6001
                }

                return Response(response_data)
        else:
            response_data = {
                "app_data": {
                    "message": "ride not found"
                },
                "StatusCode": 6001
            }

            return Response(response_data)


class UpdateRideCurrentLocationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, id):
        ride = Rides.objects.filter(id=id)
        if ride.exists():
            ride = ride[0]
            current_loc = request.data.get('current_loc')
            if current_loc:
                ride.current_location = current_loc
                ride.save()
                response_data = {
                    "app_data": {
                        "message": "location updated"
                    },
                    "StatusCode": 6000
                }

                return Response(response_data)
            else:
                response_data = {
                    "app_data": {
                        "message": "Give a valid location"
                    },
                    "StatusCode": 6001
                }

                return Response(response_data)
        else:
            response_data = {
                "app_data": {
                    "message": "ride not found"
                },
                "StatusCode": 6001
            }

            return Response(response_data)


class ListAvailableRidesWithMatchingDriversView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        rides = Rides.objects.all()
        serializer_data = RidesListWithAvailableDriversSerializer(
            rides, many=True).data

        response_data = {
            "app_data": {
                "data": serializer_data,
            },
            "StatusCode": 6000
        }

        return Response(response_data)
