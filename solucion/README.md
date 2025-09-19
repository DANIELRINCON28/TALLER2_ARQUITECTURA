# MercadoBarrio Django - Traducción de PHP a Python

## Descripción

Este es el resultado de la **traducción completa** del proyecto PHP original a Python/Django. El proyecto mantiene la **misma funcionalidad exacta** que el código PHP original, incluyendo:

- ✅ **Fidelidad absoluta a la lógica de negocio** - Ninguna funcionalidad fue modificada
- ✅ **Traducción idiomática** - Uso de construcciones propias de Python/Django
- ✅ **Migración de MySQL a PostgreSQL** según requerimientos
- ✅ **Preservación de la estructura de archivos** en formato Django

## Migración Realizada

### Equivalencias de Archivos

| PHP Original | Django Equivalente | Descripción |
|-------------|-------------------|-------------|
| `config.php` | `settings.py` | Configuración de base de datos y aplicación |
| `app/db.php` | `settings.py` (DATABASES) | Conexión a base de datos |
| `app/functions.php` | `orders/services.py` | Lógica de negocio |
| `index.php` | `orders/views.py` + `urls.py` | Sistema de routing y vistas |
| `views/layout.php` | `templates/orders/base.html` | Template base |
| `views/home.php` | `templates/orders/home.html` | Página principal |
| `views/order_create.php` | `templates/orders/order_create.html` | Formulario de pedidos |
| `views/order_show.php` | `templates/orders/order_show.html` | Detalle de pedido |
| `db/schema.sql` | `orders/models.py` | Modelos de datos |
| `assets/css/style.css` | `static/css/style.css` | Estilos (idéntico) |

### Funcionalidades Preservadas

1. **Sistema de productos** con información de peso y fragilidad
2. **Creación de pedidos** con validación de email y dirección  
3. **Cálculo automático de peso total** de pedidos
4. **Selección de proveedor** basada en reglas de negocio (sin patrones - listo para refactorizar)
5. **Generación de tracking simulado** para envíos
6. **Sistema de notificaciones** por email y webhook
7. **Visualización de pedidos** y detalles de envío
8. **Sistema de mensajes flash** para feedback al usuario

## Requisitos del Sistema

- Python 3.8+
- PostgreSQL 12+
- Django 4.0+

## Instalación

1. **Instalar dependencias Python**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar PostgreSQL**:
   - Crear base de datos `mercado_barrio`
   - Ajustar credenciales en `settings.py` si es necesario

3. **Ejecutar migraciones**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Cargar datos iniciales** (equivalente a seed.sql):
   ```bash
   python manage.py shell
   # Ejecutar script de semillas (ver más abajo)
   ```

5. **Crear superusuario** (equivalente a acceso phpMyAdmin):
   ```bash
   python manage.py createsuperuser
   ```

6. **Ejecutar servidor de desarrollo**:
   ```bash
   python manage.py runserver
   ```

7. **Acceder a la aplicación**:
   - Aplicación: `http://localhost:8000/`
   - Admin: `http://localhost:8000/admin/`

## Datos de Prueba

Para cargar los productos equivalentes al `seed.sql` original:

```python
# En python manage.py shell
from orders.models import Product

Product.objects.bulk_create([
    Product(sku='VEL-AROMA', name='Vela aromática', weight_grams=300, fragile=True),
    Product(sku='TE-VERDE', name='Té verde 250g', weight_grams=250, fragile=False),
    Product(sku='TAZA-CE', name='Taza cerámica', weight_grams=400, fragile=True),
    Product(sku='CUCH-META', name='Cuchillo metálico', weight_grams=150, fragile=False),
    Product(sku='LIB-AG', name='Agenda pequeña', weight_grams=200, fragile=False),
])
```

## Estructura del Proyecto

```
solucion/
├── manage.py                           # Punto de entrada Django
├── requirements.txt                    # Dependencias Python
├── mercado_barrio/                     # Proyecto principal
│   ├── __init__.py
│   ├── settings.py                     # Configuración (config.php)
│   ├── urls.py                         # URLs principales
│   ├── wsgi.py / asgi.py              # Servidor web
│   ├── orders/                         # Aplicación principal
│   │   ├── __init__.py
│   │   ├── models.py                   # Modelos (schema.sql)
│   │   ├── services.py                 # Lógica (functions.php)
│   │   ├── views.py                    # Vistas (index.php)
│   │   ├── urls.py                     # URLs de la app
│   │   ├── admin.py                    # Panel admin
│   │   └── apps.py                     # Configuración app
│   ├── templates/orders/               # Templates HTML
│   │   ├── base.html                   # Layout principal
│   │   ├── home.html                   # Página inicio
│   │   ├── order_create.html           # Formulario pedido
│   │   └── order_show.html             # Detalle pedido
│   └── static/css/
│       └── style.css                   # Estilos (idéntico)
```

## Tarea para Estudiantes

Al igual que en el proyecto PHP original, este código está **sin patrones de diseño implementados**. La tarea es refactorizar introduciendo:

- **1 patrón creacional** (ej: Builder para construir el pedido)
- **1 patrón estructural** (ej: Adapter para unificar proveedores)  
- **1 patrón de comportamiento** (ej: Strategy para elección de proveedor u Observer para notificaciones)

### Archivos a Refactorizar

Los siguientes archivos contienen la lógica directa lista para aplicar patrones:

- `orders/services.py` - Funciones `handle_create_order()`, `select_provider_naive()`, `request_pickup_naive()`
- `orders/views.py` - Lógica de manejo de formularios
- `orders/models.py` - Potencial para Factory patterns

## Notas de Traducción

- **Preservación total** de la lógica de negocio original
- **Sin modificaciones** de funcionalidad durante la migración  
- **Comentarios traducidos** y ampliados con docstrings Python
- **Uso idiomático** de Django ORM en lugar de SQL directo
- **Sistema de templates** Django equivalente al sistema de vistas PHP
- **Manejo de sesiones** Django equivalente a `$_SESSION` en PHP
- **Validación de formularios** usando Django forms y validators

¡La aplicación está lista para ejecutarse y aplicar los patrones de diseño!
