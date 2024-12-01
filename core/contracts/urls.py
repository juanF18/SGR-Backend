from django.urls import path
from . import views

urlpatterns = [
    path("contracts", views.ContractView.as_view(), name="contracts_view"),
    path(
        "contracts/<uuid:id>/",
        views.ContractDetailView.as_view(),
        name="contract_detail_view",
    ),
]
