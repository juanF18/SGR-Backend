from django.urls import path
from . import views

urlpatterns = [
    path("projects/", views.ProjectView.as_view()),
    path("projects/<uuid:id>/", views.ProjectDetail.as_view()),
]
