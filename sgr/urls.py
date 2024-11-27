"""
URL configuration for sgr project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from rest_framework import permissions
from django.urls import path
from django.urls import include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="SGR API",
        default_version="v1",
        description="Documentación de mi API usando Django REST Framework",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contacto@miempresa.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("core.roles.urls")),
    path("api/", include("core.entities.urls")),
    path("api/", include("core.users.urls")),
    path("api/", include("core.projects.urls")),
    path("api/", include("core.rubros.urls")),
    path("api/", include("core.items.urls")),
    path("api/", include("core.travels.urls")),
    path("api/", include("core.persons.urls")),
    path("api/", include("core.counterparts.urls")),
    path("api/", include("core.activities.urls")),
    path("api/", include("core.comments.urls")),
    path("api/", include("core.tasks.urls")),
    path("api/", include("core.detailContracts.urls")),
    path("api/", include("core.contracts.urls")),
    path("api/", include("core.cdps.urls")),
    path("api/", include("core.movements.urls")),
    # Ruta de la documentación Swagger
    path(
        "swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"
    ),
    # También puedes habilitar la documentación en formato redoc:
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc-ui"),
]
