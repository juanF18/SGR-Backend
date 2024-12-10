from django.urls import path
from . import views

urlpatterns = [
    path("tasks", views.TaskView.as_view(), name="tasks_view"),
    path(
        "tasks/<uuid:task_id>", views.TaskDetailView.as_view(), name="task_detail_view"
    ),
    path(
        "tasks/?activity_id=<uuid:activity_id>",
        views.TaskByActivityView.as_view(),
        name="tasks_by_activity_view",
    ),
]
