from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path("roles/", views.RoleView.as_view(), name="roles_view"),
    path("roles/<int:id>/", views.RoleDetailView.as_view(), name="role_detail_view"),
=======
    path('create/', views.create, name='create'),
    path('list/', views.list, name='list'),
    path('update/<int:id>/', views.update, name='update'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('detail/<int:id>/', views.detail, name='detail'),
>>>>>>> develop
]
