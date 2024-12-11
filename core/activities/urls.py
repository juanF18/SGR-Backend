from django.urls import path
from .views import ActivityByProjectView, ActivityDetailView, ActivityView

urlpatterns = [
    path("activities", ActivityView.as_view(), name="activities_view"),
    path(
        "activities/<uuid:id>",
        ActivityDetailView.as_view(),
        name="activity_detail_view",
    ),
    path(
        "activities/project/<uuid:project_id>",
        ActivityByProjectView.as_view(),
        name="activities_by_project_view",
    ),
]
