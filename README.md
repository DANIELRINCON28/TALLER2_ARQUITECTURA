# TALLER 2 - ARQUITECTURA DE SOFTWARE

## 📁 Estructura del Proyecto

Este repositorio contiene dos implementaciones del sistema MercadoBarrio siguiendo principios de arquitectura profesional, con **patrones de diseño** y **arquitectura limpia**.

## ⭐ Características Destacadas

- ✅ **Arquitectura Limpia** con separación de responsabilidades
- ✅ **Patrones de Diseño** profesionales (Builder, Adapter, Strategy, Observer)
- ✅ **Principios SOLID** aplicados correctamente
- ✅ **Código Mantenible** y fácil de extender
- ✅ **Testabilidad Mejorada** con módulos aislados
- ✅ **Documentación Completa** con diagramas y ejemplos

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
│       │           ├── creational/   # Patrones de Creación
│       │           │   ├── __init__.py
│       │           │   └── builder.py  # OrderBuilder (231 líneas)
│       │           ├── structural/   # Patrones Estructurales
│       │           │   ├── __init__.py
│       │           │   └── adapter.py  # Adapters + Factory (280 líneas)
│       │           └── behavioral/   # Patrones de Comportamiento
│       │               ├── __init__.py
│       │               ├── strategy.py # Estrategias (340 líneas)
│       │               └── observer.py # Observadores (310 líneas)
│       │
│       ├── docs/                     # 📚 Documentación técnica
│       │   ├── ARQUITECTURA_PATRONES.md    # Guía completa
│       │   ├── DIAGRAMA_ARQUITECTURA.md    # Diagramas ASCII
│       │   └── RESUMEN_REFACTORIZACION.md  # Resumen del trabajo
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

#### 🔨 Builder (Creacional)
- **Archivo**: `patterns/creational/builder.py`
- **Responsabilidad**: Construcción compleja de pedidos con validaciones
- **Clase Principal**: `OrderBuilder`
- **Features**: Validación de datos, cálculo de pesos, generación de códigos

#### 🔌 Adapter (Estructural)
- **Archivo**: `patterns/structural/adapter.py`
- **Responsabilidad**: Unificar APIs heterogéneas de proveedores de envío
- **Proveedores**: MotoYA, EcoBike, PaqueteríaZ
- **Features**: Interfaz común, Factory pattern, extensibilidad

#### 📊 Strategy (Comportamental)
- **Archivo**: `patterns/behavioral/strategy.py`
- **Responsabilidad**: Algoritmos intercambiables de selección de proveedor
- **Estrategias**: Standard, EcoFriendly, CostOptimized, WeightBased
- **Features**: Cambio dinámico, fácil extensión

#### 🔔 Observer (Comportamental)
- **Archivo**: `patterns/behavioral/observer.py`
- **Responsabilidad**: Notificaciones multi-canal automáticas
- **Observadores**: Email, Webhook, SMS, Logging
- **Features**: Desacoplamiento, notificación automática

## 📚 Documentación

- **`docs/Actividad.md`**: Requerimientos funcionales y no funcionales
- **`docs/ARQUITECTURA_PATRONES.md`**: Documentación completa de patrones
- **`docs/DIAGRAMA_ARQUITECTURA.md`**: Diagramas visuales de la arquitectura
- **`docs/RESUMEN_REFACTORIZACION.md`**: Resumen del trabajo de refactorización
- **`apps/core/patterns/README.md`**: Guía rápida de uso de patrones

## 🎯 Principios SOLID Aplicados

✅ **Single Responsibility**: Cada clase tiene una única responsabilidad  
✅ **Open/Closed**: Abierto para extensión, cerrado para modificación  
✅ **Liskov Substitution**: Los subtipos son intercambiables  
✅ **Interface Segregation**: Interfaces específicas y pequeñas  
✅ **Dependency Inversion**: Depende de abstracciones, no de concreciones

## 🚀 Uso Rápido

### Crear un Pedido con Patrones

```python
from apps.core.services import handle_create_order

order_id = handle_create_order(
    input_data={
        'customer_email': 'cliente@email.com',
        'address': 'Calle 123, Ciudad',
        'priority': 'normal',
        'fragility': 'ninguna',
        'items': {'1': 2, '2': 3}  # {product_id: quantity}
    },
    strategy_type='eco'  # 'standard' | 'eco' | 'cost'
)
```

### Usar Facade (Interface Simplificada)

```python
from apps.core.services import OrderService

service = OrderService(strategy_type='cost')
order_info = service.create_order(
    customer_email='cliente@email.com',
    address='Calle 123',
    priority='urgente',
    fragility='alta',
    items={'1': 2}
)
```

## 📊 Métricas de Calidad

| Aspecto | Antes | Después | Mejora |
|---------|-------|---------|--------|
| **Líneas en services.py** | ~1000 | 167 | **-83%** |
| **Archivos de patrones** | 0 | 4 módulos | +4 |
| **Documentación** | 0 | 4 archivos | +4 |
| **Testabilidad** | Difícil | Fácil | ✅ |
| **Principios SOLID** | Violados | Cumplidos | ✅ |

### Presentación (`templates/` o `views/`)
- Plantillas HTML
- Layouts y componentes visuales
- Separación de la capa de presentación

### Recursos Públicos (`public/` o `static/`)
- Punto de entrada de la aplicación
- CSS, JavaScript, imágenes
- Assets accesibles desde el navegador

### Base de Datos (`database/`)
- Esquemas y migraciones
- Scripts de inicialización
- Datos de prueba (seeds)

---

