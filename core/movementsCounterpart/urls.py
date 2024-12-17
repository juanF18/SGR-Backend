from django.urls import path
from . import views

urlpatterns = [
    path(
        "movementsCounterpart",
        views.MovementCounterpartView.as_view(),
        name="movements_counterpart_view",
    ),
    path(
        "movementsCounterpart/<uuid:id>",
        views.MovementsCounterpartDetailView.as_view(),
        name="movement_counterpart_detail_view",
    ),
    path(
        "movementsCounterpart/project/<uuid:project_id>",
        views.MovementsCounterpartByProjectId.as_view(),
        name="movement_counterpart-by-project",
    ),
    path(
        "movementsCounterpart/sum_by_project/<uuid:project_id>",
        views.MovementsCounterpartSumByProjectId.as_view(),
        name="movements_counterpart-sum-by-project",
    ),
]
