# TALLER 2 - ARQUITECTURA DE SOFTWARE

## Estructura del Proyecto

Este repositorio contiene dos implementaciones del sistema MercadoBarrio siguiendo principios de arquitectura profesional, con **patrones de diseño** y **arquitectura limpia**.

```
TALLER2_ARQUITECTURA/
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
│       │       ├── services.py       # ⭐ Orquestación (167 líneas)
│       │       ├── views.py          # Vistas/controladores
│       │       ├── urls.py           # Rutas de la app
│       │       ├── tests.py          # Tests unitarios
│       │       ├── migrations/       # Migraciones de BD
│       │       ├── management/       # Comandos personalizados
│       │       │   └── commands/
│       │       │       └── poblar_datos.py
│       │       └── patterns/         # 🎨 PATRONES DE DISEÑO
│       │           ├── __init__.py
│       │           ├── README.md     # Guía de uso
│       │           ├── creacional/   # Patrones de Creación
│       │           │   ├── __init__.py
│       │           │   └── builder.py  # OrderBuilder (231 líneas)
│       │           ├── estructural/   # Patrones Eestructurales
│       │           │   ├── __init__.py
│       │           │   └── adapter.py  # Adapters + Factory (280 líneas)
│       │           └── comportamental/   # Patrones de Comportamiento
│       │               ├── __init__.py
│       │               ├── strategy.py # Estrategias (340 líneas)
│       │               └── observer.py # Observadores (310 líneas)
│       │
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
│       │── ejecucion_patrones.py     # Script de demostracion            
│       ├── manage.py                 # CLI de Django
│       ├── requirements.txt          # Dependencias Python
│       └── .gitignore
│
└── venv/                             # Entorno virtual Python (no versionado)

```

##  Organización por Responsabilidades

### Configuraciones (`config/`)
- Archivos de configuración de base de datos
- Settings de frameworks
- Variables de entorno
- Configuraciones de aplicación

### Lógica de Negocio (`src/` o `apps/`)
- **Controllers**: Manejan peticiones HTTP y respuestas
- **Models**: Definición de entidades y acceso a datos  
- **Services**: Lógica de negocio y reglas de aplicación
- **Patterns**: Patrones de diseño (Builder, Adapter, Strategy, Observer)

### Patrones de Diseño Implementados (`apps/core/patterns/`)

#### Builder (Creacional)
- **Archivo**: `patterns/creacional/builder.py`
- **Responsabilidad**: Construcción compleja de pedidos con validaciones
- **Clase Principal**: `OrderBuilder`
- **Features**: Validación de datos, cálculo de pesos, generación de códigos

#### Adapter (Eestructural)
- **Archivo**: `patterns/estructural/adapter.py`
- **Responsabilidad**: Unificar APIs heterogéneas de proveedores de envío
- **Proveedores**: MotoYA, EcoBike, PaqueteríaZ
- **Features**: Interfaz común, Factory pattern, extensibilidad

#### Strategy (Comportamental)
- **Archivo**: `patterns/comportamental/strategy.py`
- **Responsabilidad**: Algoritmos intercambiables de selección de proveedor
- **Estrategias**: Standard, EcoFriendly, CostOptimized, WeightBased
- **Features**: Cambio dinámico, fácil extensión

#### Observer (Comportamental)
- **Archivo**: `patterns/comportamental/observer.py`
- **Responsabilidad**: Notificaciones multi-canal automáticas
- **Observadores**: Email, Webhook, SMS, Logging
- **Features**: Desacoplamiento, notificación automática

## Instalación y Ejecución

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

### 4. Restaurar base de datos
```
Dado que la base de datos fue trabajada en PostgresSQL, es requerido usar el motor de postgres
y restablecer la BD desde el archivo Backup_BD.sql
```

### 5. Ejecutar servidor
```bash
python manage.py runserver
```
### 6. Ejecutar script 
```bash
python ejecucion_patrones.py
```

Acceder a: `http://localhost:8000`


