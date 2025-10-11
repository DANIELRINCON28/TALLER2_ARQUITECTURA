# Documentación: Arquitectura Limpia con Patrones de Diseño

Inicialmente el archivo `services.py` original contenía **toda la lógica** en un único archivo de ~1000 líneas. Por medio de la separacion de responsabilidades y distribucion en diferentes directorios se logró implementar una mejor estructura:

### Estructura de los patrones

apps/core/
├── services.py                    # Orquestación y facade (167 líneas)
└── patterns/                      # Patrones extraídos
    ├── __init__.py               # Exports centralizados
    ├── creacional/               # Patrones de creación
    │   ├── __init__.py
    │   └── builder.py            # OrderBuilder
    ├── estructural/               # Patrones eestructurales
    │   ├── __init__.py
    │   └── adapter.py            # ShippingAdapters + Factory
    └── comportamental/               # Patrones de comportamiento
        ├── __init__.py
        ├── strategy.py           # Estrategias de selección
        └── observer.py           # Sistema de notificaciones
```