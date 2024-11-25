from django.urls import path
from . import views

urlpatterns = [
    path("travels", views.TravelView.as_view(), name="travels_view"),
    path(
        "travels/<int:id>/", views.TravelDetailView.as_view(), name="travel_detail_view"
    ),
]
