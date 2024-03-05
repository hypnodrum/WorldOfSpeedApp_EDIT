from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('WorldOfSpeedApp.web.urls')),
    path("car/", include('WorldOfSpeedApp.cars.urls')),
    path("profile/", include('WorldOfSpeedApp.profiles.urls'))
]
