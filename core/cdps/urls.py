from django.urls import path
from . import views

urlpatterns = [
    path("cdps", views.CdpsView.as_view(), name="cdps_view"),
    path("cdps/<uuid:id>/", views.CdpsDetailView.as_view(), name="cdp_detail_view"),
    path("cdps/<uuid:cdps_id>/<uuid:user_id>/", views.CdpsGeneratePdf.as_view(), name="cdp_pdf_view"),
]
