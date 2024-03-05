from django.urls import path
from WorldOfSpeedApp.profiles.views import create_profile, DeleteProfileView, LoginUserView, LogoutUserView, \
  edit_profile, ProfileDetailView

urlpatterns = (
    path("create/", create_profile, name="create_profile"),
    path("login/", LoginUserView.as_view(template_name="profiles/login.html"), name="login"),
    path("details/<int:pk>", ProfileDetailView.as_view(), name="details_profile"),
    path("edit/", edit_profile, name="edit_profile"),
    path("delete/<int:pk>", DeleteProfileView.as_view(), name="delete_profile"),
    path("logout/", LogoutUserView.as_view(), name="logout"),
)
