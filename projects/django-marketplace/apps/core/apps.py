"""
Configuración de la aplicación core.
Equivalente a la organización modular del proyecto PHP.
"""
from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    Configuración de la aplicación core.
    Maneja la funcionalidad principal equivalente a functions.php.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    verbose_name = 'Sistema de Pedidos MercadoBarrio'