from django.urls import path
from . import views

urlpatterns = [
    path("activities", views.ActivityView.as_view(), name="activities_view"),
    path(
        "activities/<int:id>/",
        views.ActivityDetailView.as_view(),
        name="activity_detail_view",
    ),
]
