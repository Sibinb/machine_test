from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('api.v1.accounts.urls')),
    path('ride/',include('api.v1.ride.urls')),
    path('driver/',include('api.v1.driver.urls')),
]
