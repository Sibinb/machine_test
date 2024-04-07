from django.urls import path
from .views import RidesListView,CreateRideView,ListSingleRideView,RideStatusUpdateView,UpdateRideCurrentLocationView,ListAvailableRidesWithMatchingDriversView

app_name = 'api-ride'

urlpatterns = [
    path('list-rides/',RidesListView.as_view(),name='list-ride'),
    path('list-sigle-ride/<int:id>',ListSingleRideView.as_view(),name='list-single-ride'),
    path('create-ride/',CreateRideView.as_view(),name='create-ride'),
    path('ride-status-update/<int:id>/',RideStatusUpdateView.as_view(),name='ride-status-update'),
    path('ride-current-location-update/<int:id>/',UpdateRideCurrentLocationView.as_view(),name='ride-curent-location-update'),
    path('list-match-drivers/',ListAvailableRidesWithMatchingDriversView.as_view(),name='list-match-drivers'),
]
