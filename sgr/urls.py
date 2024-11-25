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
from django.urls import path
from django.urls import include

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
]
