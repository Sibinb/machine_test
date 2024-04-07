from django.contrib import admin
from .models import *


class DriverAdmin(admin.ModelAdmin):
    list_display = ('id',"location",
                    "status"
                    )


admin.site.register(Driver,DriverAdmin)
