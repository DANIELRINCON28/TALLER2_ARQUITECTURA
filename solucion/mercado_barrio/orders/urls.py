"""
URLs para la aplicación orders.
Traducción directa del sistema de routing del index.php con el parámetro 'r'.
Equivalente al switch/case que maneja ?r=home, ?r=order/create, ?r=order/show
"""
from django.urls import path
from . import views

# Equivalente al sistema de routing en index.php: $route = $_GET['r'] ?? 'home';
urlpatterns = [
    # Equivalente a: case 'home'
    path('', views.home_view, name='home'),
    
    # Equivalente a: case 'order/create'
    path('order/create/', views.order_create_view, name='order_create'),
    
    # Equivalente a: case 'order/show' con $_GET['id']
    path('order/show/<int:order_id>/', views.order_show_view, name='order_show'),
]