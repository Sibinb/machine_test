from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import Driver
from ride.models import Rides


class TestDriverApp(APITestCase):
    def setUp(self):
        self.driver = Driver.objects.create(
            username="driver", location="kochi")
        self.driver.set_password('test')
        self.driver.save()

    def test_driver_list_endpoint(self):
        url = reverse('api-driver:list-drivers')
        response = self.client.get(url).data
        status_code = response['StatusCode']
        id_of_first_data = response['app_data']['data'][0]['id']
        self.assertEqual(status_code, 6000)
        self.assertEqual(id_of_first_data, self.driver.pk)

    def test_driver_status_update_endpoint(self):
        url = reverse('api-driver:update-driver-status', args=[self.driver.pk])
        data = {'status': "offline"}
        response = self.client.post(url, data, format='json').data
        status_code = response['StatusCode']
        self.assertEqual(6000, status_code)

class AcceptRideRequestTest(APITestCase):
    def setUp(self):
        self.driver = Driver.objects.create(
            username="driver", location="kochi")
        self.driver.set_password('test')
        self.driver.save()
        
        self.ride = Rides.objects.create(
        dropoff_location="kakkanad", rider='test', pickup_location='kochi')
        
    def test_accept_ride_request_endpoint(self):
        url = reverse('api-driver:accept-ride', args=[self.ride.pk,self.driver.pk])
        response = self.client.post(url).data
        status_code = response['StatusCode']
        message = response['app_data']['message']
        self.assertEqual(6000, status_code)
        self.assertEqual("ride is accepted", message)
