from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

class TestLoginAndRegistration(APITestCase):
    
    def setUp(self):
        self.user1 = User.objects.create(username="test")
        self.user1.set_password('test')
        self.user1.save()
        
    def test_registration_end_point(self):
        url = reverse('api-accounts:register')
        data = {'username':"test2",'password':"test2"}
        response = self.client.post(url, data,format='json').data
        status_code = response['StatusCode']
        self.assertEqual(6000,status_code)
        
    def test_registration_duplicate_entry(self):
        url = reverse('api-accounts:register')
        data = {'username':"test",'password':"test2"}
        response = self.client.post(url, data,format='json').data
        status_code = response['StatusCode']
        self.assertEqual(6001,status_code)
        
    def test_login_end_point(self):
        url = reverse('api-accounts:login')
        data = {'username':"test",'password':"test"}
        response = self.client.post(url,data,format='json').data
        status_code = response['StatusCode']
        self.assertEqual(6000,status_code)
        
    def test_login_with_wrong_credentials(self):
        url = reverse('api-accounts:login')
        data = {'username':"test",'password':"test1"}
        response = self.client.post(url,data,format='json').data
        status_code = response['StatusCode']
        self.assertEqual(6001,status_code)
    
        
        