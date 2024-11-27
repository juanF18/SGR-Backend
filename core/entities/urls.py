from django.urls import path
from . import views

urlpatterns = [
    path("entities/", views.EntityView.as_view(), name="entities_view"),
    path("entities/<int:id>/", views.EntityDetailView.as_view(), name="entity_detail_view"),
]
