from django.urls import path
from . import views

urlpatterns = [
    path("movements", views.MovementView.as_view(), name="movements_view"),
    path(
        "movements/<uuid:id>",
        views.MovementDetailView.as_view(),
        name="movement_detail_view",
    ),
    path(
        "movements/project/<uuid:project_id>",
        views.MovementsByProjectId.as_view(),
        name="movement-by-project",
    ),
    path(
        "movements/sum_by_project/<uuid:project_id>",
        views.MovementsSumByProjectId.as_view(),
        name="movements-sum-by-project",
    ),
]
