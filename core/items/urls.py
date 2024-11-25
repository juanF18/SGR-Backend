from django.urls import path
from . import views

urlpatterns = [
    path("items/", views.ItemView.as_view(), name="items_view"),
    path("items/<int:id>/", views.ItemDetailView.as_view(), name="item_detail_view"),
]
