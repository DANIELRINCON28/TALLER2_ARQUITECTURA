# Django Marketplace - MercadoBarrio

## 📋 Descripción
Implementación en Django (Python) del sistema MercadoBarrio para gestión de pedidos y entregas.

## 🏗️ Arquitectura del Proyecto

### Estructura de Directorios

```
django-marketplace/
├── config/                  # ⚙️ Configuraciones del proyecto
│   ├── __init__.py
│   ├── settings.py          # Configuración de Django
│   ├── urls.py              # URLs principales
│   └── wsgi.py              # WSGI application
├── apps/                    # 💼 Aplicaciones Django
│   └── core/                # App principal
│       ├── models.py        # Modelos de datos
│       ├── views.py         # Vistas/controladores
│       ├── services.py      # Lógica de negocio
│       ├── urls.py          # URLs de la app
│       ├── admin.py         # Configuración admin
│       ├── migrations/      # Migraciones de BD
│       └── management/      # Comandos personalizados
├── templates/               # 🎨 Plantillas HTML
│   └── orders/
├── static/                  # 🌐 Archivos estáticos
│   └── css/
├── manage.py                # CLI de Django
└── requirements.txt         # Dependencias
```

### Separación de Responsabilidades

#### 📁 `/config` - Configuración del Proyecto
Configuración centralizada de Django:
- `settings.py`: Base de datos, apps, middleware, static files
- `urls.py`: Rutas principales del proyecto
- `wsgi.py`: Configuración WSGI para producción

#### 📁 `/apps` - Aplicaciones
Organización modular por funcionalidad:

**Core App** - Funcionalidad principal:
- `models.py`: Modelos de datos (Pedido, Cliente, Proveedor)
- `services.py`: Lógica de negocio y patrones de diseño
- `views.py`: Controladores de vistas
- `urls.py`: Rutas específicas de la app
- `admin.py`: Configuración del panel de administración
- `migrations/`: Migraciones de base de datos
- `management/commands/`: Comandos CLI personalizados
  - `poblar_datos.py`: Comando para poblar datos de prueba

#### 📁 `/templates` - Vistas
Plantillas HTML organizadas por módulo:
- `orders/`: Vistas de pedidos
  - `base.html`: Plantilla base
  - `home.html`: Página principal
  - `order_create.html`: Crear pedido
  - `order_show.html`: Mostrar pedido

#### 📁 `/static` - Recursos Estáticos
Archivos CSS, JavaScript, imágenes:
- `css/`: Hojas de estilo
- `js/`: Scripts (si se agregan)
- `img/`: Imágenes (si se agregan)

## 🚀 Instalación y Ejecución

### 1. Crear entorno virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar base de datos
```bash
python manage.py migrate
```

### 4. Poblar datos de prueba
```bash
python manage.py poblar_datos
```

### 5. Crear superusuario (opcional)
```bash
python manage.py createsuperuser
```

### 6. Ejecutar servidor
```bash
python manage.py runserver
```

Acceder a: `http://localhost:8000`

## 📌 Patrones Implementados
- [Documentar patrones usados aquí]
- Patrón Builder
- Patrón Strategy
- Patrón Observer

## 🔗 Endpoints Principales
- `/` - Inicio
- `/orders/create/` - Crear pedido
- `/orders/<id>/` - Ver detalle de pedido
- `/admin/` - Panel de administración

## 🧪 Testing
```bash
python manage.py test apps.core
```

## 📝 Comandos Útiles

### Crear nueva migración
```bash
python manage.py makemigrations
```

### Aplicar migraciones
```bash
python manage.py migrate
```

### Shell interactivo
```bash
python manage.py shell
```

### Poblar datos
```bash
python manage.py poblar_datos
```

## 🏛️ Arquitectura Django

Este proyecto sigue el patrón **MVT (Model-View-Template)** de Django:
- **Models** (`models.py`): Capa de datos
- **Views** (`views.py`): Lógica de controladores
- **Templates** (`templates/`): Presentación
- **Services** (`services.py`): Lógica de negocio (patrón adicional)

La separación de `services.py` permite aplicar patrones de diseño sin contaminar las vistas.
