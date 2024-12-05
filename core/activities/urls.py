from django.urls import path
from . import views

urlpatterns = [
    path("activities", views.ActivityView.as_view(), name="activities_view"),
    path(
        "activities/<uuid:id>",
        views.ActivityDetailView.as_view(),
        name="activity_detail_view",
    ),
    path(
        "activities/<uuid:project_id>",
        views.ActivityByProjectView(),
        name="activities_by_project_view",
    ),
]
