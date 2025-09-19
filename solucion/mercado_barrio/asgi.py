"""
ASGI config for mercado_barrio project.
Configuración ASGI equivalente a la configuración de servidor web en PHP.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mercado_barrio.settings')

application = get_asgi_application()