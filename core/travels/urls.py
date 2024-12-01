from django.urls import path
from . import views

urlpatterns = [
    path("travels", views.TravelView.as_view(), name="travels_view"),
    path(
        "travels/<uuid:id>/", views.TravelDetailView.as_view(), name="travel_detail_view"
    ),
]
