from django.urls import path
from . import views

urlpatterns = [
    path("movements", views.MovementView.as_view(), name="movements_view"),
    path(
        "movements/<int:id>/",
        views.MovementDetailView.as_view(),
        name="movement_detail_view",
    ),
]
