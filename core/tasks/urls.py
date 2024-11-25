from django.urls import path
from . import views

urlpatterns = [
    path("tasks", views.TaskView.as_view(), name="tasks_view"),
    path("tasks/<int:id>/", views.TaskDetailView.as_view(), name="task_detail_view"),
]
