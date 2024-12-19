from django.urls import path
from .views import (
    MovementCounterpartView,
    MovementCounterpartDetailView,
    MovementCounterpartSumView,
)

urlpatterns = [
    path(
        "movement-counterparts",
        MovementCounterpartView.as_view(),
        name="movement-counterparts",
    ),
    path(
        "movement-counterparts/<uuid:movement_id>",
        MovementCounterpartDetailView.as_view(),
        name="movement-counterpart-detail",
    ),
    path(
        "movement-counterparts/sum",
        MovementCounterpartSumView.as_view(),
        name="movement-couterpart-sum",
    ),
]
