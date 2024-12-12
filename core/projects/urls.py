from django.urls import path
from . import views

urlpatterns = [
    path("projects/", views.ProjectView.as_view()),
    path("projects/<uuid:id>/", views.ProjectDetail.as_view()),
    path(
        "projects/entity/<uuid:entity_id>/",
        views.ProjectByEntityView.as_view(),
        name="projects-by-entity",
    ),
]
