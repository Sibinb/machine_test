from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from driver.models import Driver
from ride.models import Rides
from api.v1.ride.serializers import RidesListSerializer
from .serializers import DriverListSerializer


class RegisterDriverView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        name = request.data.get('name')
        password = request.data.get('password')
        location = request.data.get('location')

        if name and password and location:
            print("hai")
            print(Driver.objects.filter(username=name).exists())
            if (not Driver.objects.filter(username=name).exists()):
                driver = Driver.objects.create_user(
                    username=name, password=password, location=location)
                if driver:
                    response_data = {"message": "Registration successful"}
                    return Response({"app_data": response_data, "StatusCode": 6000})
                else:
                    response_data = {"message": "Failed to register user"}
                    return Response({"app_data": response_data, "StatusCode": 6001})
            else:
                response_data = {"message": "Name already in use"}
                return Response({"app_data": response_data, "StatusCode": 6001})
        else:
            response_data = {"message": "Fill all fields"}
            return Response({"app_data": response_data, "StatusCode": 6001})


class LoginDriverView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        driver = authenticate(username=username, password=password)

        if driver is not None:
            # sending jwt token
            response_data = {"status": "Success"}
            return Response({"app_data": response_data, "StatusCode": 6000})
        else:
            response_data = {"status": "Failed",
                             "message": "Invalid credentials"}
            return Response({"app_data": response_data, "StatusCode": 6001})


class ListDriverView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        drivers = Driver.objects.all()
        serializer_data = DriverListSerializer(drivers, many=True).data

        response_data = {
            "app_data": {
                "data": serializer_data
            },
            "StatusCode": 6000
        }

        return Response(response_data)


class DriverStatusUpdateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, id):
        driver = Driver.objects.filter(id=id)
        if driver.exists():
            driver = driver[0]
            status = request.data.get('status')
            if status:
                driver.status = status
                driver.save()
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
                    "message": "driver not found"
                },
                "StatusCode": 6001
            }

            return Response(response_data)


class ListRidesForDriverView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        driver = Driver.objects.filter(id=id)
        if driver.exists():
            driver = driver[0]
            available_rides = Rides.objects.filter(
                status='available', pickup_location=driver.location)

            if available_rides.exists():
                serializer_data = RidesListSerializer(
                    available_rides, many=True).data
                response_data = {
                    "app_data": {
                        "date": serializer_data
                    },
                    "StatusCode": 6001
                }

                return Response(response_data)
            else:
                response_data = {
                    "app_data": {
                        "message": "no rides available"
                    },
                    "StatusCode": 6001
                }

            return Response(response_data)

        else:
            response_data = {
                "app_data": {
                    "message": "driver not found"
                },
                "StatusCode": 6001
            }

            return Response(response_data)


class AcceptRideView(APIView):
    permission_classes = [AllowAny]
    
    def post(self,request,id,driverid):
        
        ride = Rides.objects.filter(id=id)
        driver = Driver.objects.filter(id=driverid)
        
        if ride.exists():
            ride = ride[0]
            if ride.status == 'available':
               if driver.exists():
                   driver = driver[0]
                   
                   if driver.status == 'available':
                       # updating ride status
                       ride.driver = driver
                       ride.status = 'started'
                       ride.save()
                       
                       #update driver status
                       driver.status = 'on-trip'
                       driver.save()
                       
                       response_data = {"message": "ride is accepted"}
                       return Response({"app_data": response_data, "StatusCode": 6000})
                       
                   else:
                       response_data = {"message": "driver is not available"}
                       return Response({"app_data": response_data, "StatusCode": 6001})
               else:
                   response_data = {"message": "driver not found"}
                   return Response({"app_data": response_data, "StatusCode": 6001})
            else:
                response_data = {"message": "ride is not available"}
                return Response({"app_data": response_data, "StatusCode": 6001})
        else:
            response_data = {"message": "ride not found"}
            return Response({"app_data": response_data, "StatusCode": 6001})
        