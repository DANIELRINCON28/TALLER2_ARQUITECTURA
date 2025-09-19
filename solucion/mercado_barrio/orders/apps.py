"""
Configuración de la aplicación orders.
Equivalente a la organización modular del proyecto PHP.
"""
from django.apps import AppConfig


class OrdersConfig(AppConfig):
    """
    Configuración de la aplicación orders.
    Maneja la funcionalidad de pedidos equivalente a functions.php.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'
    verbose_name = 'Sistema de Pedidos MercadoBarrio'