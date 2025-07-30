# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('add_transaction/', views.add_transaction, name='add_transaction'),
    path('register/', views.register, name='register'),
    path('manage_categories/', views.manage_categories, name='manage_categories'),
    path('delete_category/<int:pk>/', views.delete_category, name='delete_category'),
    path('delete_transaction/<int:pk>/', views.delete_transaction, name='delete_transaction'),
]
