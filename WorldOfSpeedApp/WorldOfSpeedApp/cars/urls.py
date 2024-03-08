from django.urls import path, include
from WorldOfSpeedApp.cars.views import catalogue, create_car, DetailCarView, EditCarView, DeleteCarView

urlpatterns = (
    path("catalogue/", catalogue, name="catalogue"),
    path("create/", create_car, name="create_car"),
    path("<int:pk>/", include([
        path("details/", DetailCarView.as_view(), name="details_car"),
        path("edit/", EditCarView.as_view(), name="edit_car"),
        path("delete/", DeleteCarView.as_view(), name="delete_car")
    ])),

)
