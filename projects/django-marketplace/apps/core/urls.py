"""
URLs para la aplicación orders con PATRONES DE DISEÑO integrados.
Incluye rutas adicionales para demostrar funcionalidad de los patrones.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Rutas principales
    path('', views.home_view, name='home'),
    path('order/create/', views.order_create_view, name='order_create'),
    path('order/show/<int:order_id>/', views.order_show_view, name='order_show'),
    
    # API para demostrar patrón Observer en tiempo real
    path('api/order/<int:order_id>/status/', views.order_status_api, name='order_status_api'),
]