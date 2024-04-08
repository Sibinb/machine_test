from django.urls import path
from .views import ListDriverView, RegisterDriverView, LoginDriverView, DriverStatusUpdateView,ListRidesForDriverView,AcceptRideView

app_name = 'api-driver'

urlpatterns = [
    path('register-driver/', RegisterDriverView.as_view(), name='register-driver'),
    path('login-driver/', LoginDriverView.as_view(), name='login-driver'),
    path('list-drivers/', ListDriverView.as_view(), name='list-drivers'),
    path('update-driver-status/<int:id>/',
         DriverStatusUpdateView.as_view(), name='update-driver-status'),
    path('list-available-rides/<int:id>/', ListRidesForDriverView.as_view(), name='list-available-rides'),
    path('accept-ride/<int:id>/<int:driverid>', AcceptRideView.as_view(), name='accept-ride'),
    
]
