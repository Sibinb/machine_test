from django.db import models
from django.contrib.auth.models import Group, User

DRIVER_STATUS_CHOICES = (
    ("available",'Available'),
    ("offline",'OFFLINE'),
    ("on-trip",'On-Trip'),
)

class Driver(User):
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=255,choices=DRIVER_STATUS_CHOICES,default="available")
    
    class Meta:
        db_table = 'Driver'
