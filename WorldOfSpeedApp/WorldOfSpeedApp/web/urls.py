from django.urls import path
from WorldOfSpeedApp.web.views import index, custom_404_view

urlpatterns = (path("", index, name="index"),)


handler404 = custom_404_view