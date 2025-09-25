"""
Configuración de Django para el proyecto mercado_barrio.
Traducción directa de config.php manteniendo la misma funcionalidad.
Migrado de MySQL a PostgreSQL según requerimientos.
"""
from pathlib import Path
import os
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Equivalente a la configuración de seguridad implícita en PHP
SECRET_KEY = 'django-insecure-keep_this_secret_in_production_environment'

# SECURITY WARNING: don't run with debug turned on in production!
# Traducción de APP_DEBUG = true en config.php
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Application definition
# Equivalente a los includes/requires en index.php
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mercado_barrio.orders.apps.OrdersConfig',  # Aplicación principal equivalente a functions.php
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mercado_barrio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'mercado_barrio' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mercado_barrio.wsgi.application'

# Database configuration
# Traducción de la configuración MySQL a PostgreSQL
# Equivalente a las constantes DB_* en config.php
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mercado_barrio',  # Equivalente a DB_NAME = 'cine_patterns'
        'USER': 'postgres',        # Equivalente a DB_USER = 'root'
        'PASSWORD': 'password',            # Equivalente a DB_PASS = ''
        'HOST': '127.0.0.1',      # Equivalente a DB_HOST = '127.0.0.1'
        'PORT': '5432',
        'OPTIONS': {
            'client_encoding': 'UTF8',  # Equivalente a DB_CHARSET = 'utf8mb4'
        },
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# Equivalente a date_default_timezone_set('America/Bogota') en config.php
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# Equivalente a la carpeta assets/css en el proyecto PHP
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Messages framework configuration
# Equivalente al sistema de mensajes flash en PHP ($_SESSION['flash'])
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',  # Mantiene compatibilidad con clases CSS del PHP original
}

# Session configuration
# Equivalente a session_start() en index.php
SESSION_COOKIE_AGE = 1800  # 30 minutos
SESSION_SAVE_EVERY_REQUEST = True