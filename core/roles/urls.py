from django.urls import path
from . import views

urlpatterns = [
    path("roles/", views.RoleView.as_view(), name="roles_view"),
    path("roles/<uuid:id>/", views.RoleDetailView.as_view(), name="role_detail_view"),
]
