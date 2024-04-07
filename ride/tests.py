from django.urls import reverse
from rest_framework.test import APITestCase
from .models import Rides
from driver.models import Driver


class TestRides(APITestCase):

    def setUp(self):
        self.ride = Rides.objects.create(
            dropoff_location="kakkanad", rider='test', pickup_location='kochi')

    def test_rides_list_endpoint(self):
        url = reverse('api-ride:list-ride')
        response = self.client.get(url).data
        status_code = response['StatusCode']
        id_of_ride = response["app_data"]['data'][0]['id']
        self.assertEqual(6000, status_code)
        self.assertEqual(id_of_ride, self.ride.pk)

    def test_list_single_ride_endpoint(self):
        url = reverse('api-ride:list-single-ride', args=[1])
        response = self.client.get(url).data
        status_code = response['StatusCode']
        rider_of_ride = response["app_data"]['data']['rider']
        self.assertEqual(6000, status_code)
        self.assertEqual(rider_of_ride, self.ride.rider)

    def test_create_ride_endpoint(self):
        url = reverse('api-ride:create-ride')
        data = {"dropoff_location": "kakkanad",
            "rider": 'test2', "pickup_location": 'kochi'}
        response = self.client.post(url, data, format='json').data
        status_code = response['StatusCode']
        self.assertEqual(6000, status_code)

    def test_ride_status_update_endpoint(self):
        url = reverse('api-ride:ride-status-update', args=[self.ride.pk])
        data = {'status': "completed"}
        response = self.client.post(url, data, format='json').data
        status_code = response['StatusCode']
        self.assertEqual(6000, status_code)

    def test_ride_current_location_update_endpoint(self):
        url = reverse('api-ride:ride-curent-location-update',
                      args=[self.ride.pk])
        data = {'current_loc': "pipeline"}
        response = self.client.post(url, data, format='json').data
        status_code = response['StatusCode']
        self.assertEqual(6000, status_code)


class TestRideMacthingAlogrithm(APITestCase):
      def setUp(self):
        self.ride = Rides.objects.create(
            dropoff_location="kakkanad", rider='test', pickup_location='kochi')
        self.driver = Driver.objects.create(username="driver",location="kochi")
        self.driver.set_password('test')
        self.driver.save()

      def test_ride_matching_algorithm(self):
        url = reverse('api-ride:list-match-drivers')
        response = self.client.get(url).data
        status_code = response['StatusCode']
        driver_id = response['app_data']['data'][0]['available_drivers'][0]['id']
        self.assertEqual(6000,status_code)
        self.assertEqual(driver_id, self.driver.pk)