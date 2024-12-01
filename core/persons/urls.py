from django.urls import path
from . import views

urlpatterns = [
    path("persons", views.PersonView.as_view(), name="persons_view"),
    path(
        "persons/<uuid:id>/", views.PersonDetailView.as_view(), name="person_detail_view"
    ),
]
