from django.db import models

RIDES_STATUS_CHOICES = (
    ("completed", "Completed"),
    ("cancelled", "Cancelled"),
    ("started", "Started"),
    ("available", "Available"),
)

class Rides(models.Model):
    rider = models.TextField()
    driver = models.ForeignKey('driver.Driver',null=True,blank=True,on_delete=models.CASCADE)
    pickup_location = models.TextField(max_length=255)
    dropoff_location = models.TextField(max_length=255)
    current_location = models.TextField(max_length=255,null=True,blank=True)
    status=models.CharField(choices=RIDES_STATUS_CHOICES,max_length=255,default='available')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)