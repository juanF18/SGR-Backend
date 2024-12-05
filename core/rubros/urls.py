from django.urls import path
from . import views

urlpatterns = [
    path("rubros", views.RubroView.as_view(), name="rubros_view"),
    path(
        "rubros/<uuid:id>/", views.RubroDetailView.as_view(), name="rubro_detail_view"
    ),
    path(
        "rubros/<uuid:project_id>/",
        views.RubroProjectView.as_view(),
        name="rubro_project_view",
    ),
]
