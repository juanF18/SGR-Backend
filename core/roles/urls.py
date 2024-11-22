from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create, name='create'),
    path('list/', views.list, name='list'),
    path('update/<int:id>/', views.update, name='update'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('detail/<int:id>/', views.detail, name='detail'),
]
