from django.urls import path
from . import views

urlpatterns = [
    path(
        "detailContracts",
        views.DetailContractView.as_view(),
        name="detailContracts_view",
    ),
    path(
        "detailContracts/<uuid:id>/",
        views.DetailContractDetailView.as_view(),
        name="detailContract_detail_view",
    ),
]
