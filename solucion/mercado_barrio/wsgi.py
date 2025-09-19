"""
WSGI config for mercado_barrio project.
Configuración WSGI equivalente a la configuración de servidor web en PHP.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mercado_barrio.settings')

application = get_wsgi_application()