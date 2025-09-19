#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.
Equivalente a la configuración de XAMPP en el proyecto PHP original.
"""
import os
import sys

if __name__ == '__main__':
    """
    Punto de entrada principal de la aplicación Django.
    Reemplaza la funcionalidad del servidor web de XAMPP y el punto de entrada index.php.
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mercado_barrio.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)