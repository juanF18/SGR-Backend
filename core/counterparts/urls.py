from django.urls import path
from . import views

urlpatterns = [
    path("counterparts", views.CounterpartView.as_view(), name="counterparts_view"),
    path(
        "counterparts/<uuid:id>/",
        views.CounterpartDetailView.as_view(),
        name="counterpart_detail_view",
    ),
]
