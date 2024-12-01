from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.UserView.as_view(), name="users_view"),
    path("users/<uuid:pk>/", views.UserDetailView.as_view(), name="users_detail_view"),
    path("login/", views.LoginUserView.as_view(), name="user-login"),
]
