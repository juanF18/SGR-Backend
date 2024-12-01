from django.urls import path
from . import views

urlpatterns = [
    path("cdps", views.CdpsView.as_view(), name="cdps_view"),
    path("cdps/<uuid:id>/", views.CdpsDetailView.as_view(), name="cdp_detail_view"),
]
