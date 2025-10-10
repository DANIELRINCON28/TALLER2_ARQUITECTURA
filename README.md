# TALLER 2 - ARQUITECTURA DE SOFTWARE

## 📁 Estructura del Proyecto

Este repositorio contiene dos implementaciones del sistema MercadoBarrio siguiendo principios de arquitectura profesional:

```
TALLER2_ARQUITECTURA/
│
├── 📚 docs/                          # Documentación del proyecto
│   └── Actividad.md                  # Especificaciones y requerimientos (renombrado)
│
├── 🚀 projects/                      # Proyectos implementados
│   │
│   ├── domi/                         # Implementación original (domi)
│   │   ├── config.php                # ⚙️ Configuración principal
│   │   ├── index.php                 # 🌐 Punto de entrada
│   │   ├── README.md                 # � Documentación del ejercicio original
│   │   ├── app/                      # 💼 Código de aplicación
│   │   │   ├── db.php                # Conexión a base de datos
│   │   │   └── functions.php         # Funciones y lógica de negocio
│   │   ├── assets/                   # 🎨 Recursos estáticos
│   │   │   └── css/
│   │   │       └── style.css
│   │   ├── db/                       # 🗄️ Scripts de base de datos
│   │   │   ├── schema.sql
│   │   │   └── seed.sql
│   │   └── views/                    # 🎨 Vistas (plantillas PHP)
│   │       ├── layout.php
│   │       ├── home.php
│   │       ├── order_create.php
│   │       └── order_show.php
│   │
│   └── django-marketplace/           # Implementación Django (Python)
│       ├── config/                   # ⚙️ Configuraciones del proyecto
│       │   ├── __init__.py
│       │   ├── settings.py           # Configuración de Django
│       │   ├── urls.py               # Rutas principales
│       │   └── wsgi.py               # WSGI application
│       │
│       ├── apps/                     # 💼 Aplicaciones Django
│       │   ├── __init__.py
│       │   └── core/                 # App principal
│       │       ├── __init__.py
│       │       ├── admin.py          # Configuración admin
│       │       ├── apps.py           # Configuración app
│       │       ├── models.py         # Modelos de datos
│       │       ├── services.py       # Lógica de negocio
│       │       ├── views.py          # Vistas/controladores
│       │       ├── urls.py           # Rutas de la app
│       │       ├── tests.py          # Tests unitarios
│       │       ├── migrations/       # Migraciones de BD
│       │       └── management/       # Comandos personalizados
│       │           └── commands/
│       │               └── poblar_datos.py
│       │
│       ├── templates/                # 🎨 Plantillas HTML
│       │   └── orders/               # Vistas de pedidos
│       │       ├── base.html
│       │       ├── home.html
│       │       ├── order_create.html
│       │       └── order_show.html
│       │
│       ├── static/                   # 🌐 Archivos estáticos
│       │   └── css/
│       │       └── style.css
│       │
│       ├── manage.py                 # CLI de Django
│       ├── requirements.txt          # Dependencias Python
│       └── .gitignore
│
└── venv/                             # Entorno virtual Python (no versionado)

```

## 🎯 Organización por Responsabilidades

### ⚙️ Configuraciones (`config/`)
- Archivos de configuración de base de datos
- Settings de frameworks
- Variables de entorno
- Configuraciones de aplicación

### 💼 Lógica de Negocio (`src/` o `apps/`)
- **Controllers**: Manejan peticiones HTTP y respuestas
- **Models**: Definición de entidades y acceso a datos
- **Services**: Lógica de negocio y reglas de aplicación
- Patrones de diseño implementados

### 🎨 Presentación (`templates/` o `views/`)
- Plantillas HTML
- Layouts y componentes visuales
- Separación de la capa de presentación

### 🌐 Recursos Públicos (`public/` o `static/`)
- Punto de entrada de la aplicación
- CSS, JavaScript, imágenes
- Assets accesibles desde el navegador

### 🗄️ Base de Datos (`database/`)
- Esquemas y migraciones
- Scripts de inicialización
- Datos de prueba (seeds)

### 📚 Documentación (`docs/`)
- Especificaciones del proyecto
- Requerimientos funcionales
- Guías de implementación

---

