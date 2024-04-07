from django.contrib import admin
from .models import *


class RidesAdmin(admin.ModelAdmin):
    list_display = ('id', 'rider', "driver",
                    "pickup_location",
                    "dropoff_location",
                    "status",
                    "created_at",
                    "updated_at")


admin.site.register(Rides,RidesAdmin)
