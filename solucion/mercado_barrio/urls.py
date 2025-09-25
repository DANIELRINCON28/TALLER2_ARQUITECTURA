"""
Configuración principal de URLs para el proyecto mercado_barrio.
Equivalente al sistema de enrutamiento en index.php con el parámetro 'r'.
"""
from django.contrib import admin
from django.urls import path, include

# Equivalente al switch/case para las rutas en index.php
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mercado_barrio.orders.urls')),  # Incluye todas las rutas de la aplicación orders
]