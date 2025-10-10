# Documentación: Arquitectura Limpia con Patrones de Diseño

## 📋 Resumen de la Refactorización

Este documento describe la transformación del sistema desde un archivo monolítico `services.py` hacia una **arquitectura limpia** usando patrones de diseño.

---

## 🎯 Problema Original

El archivo `services.py` original contenía **toda la lógica** en un único archivo de ~1000 líneas:
- ❌ Violación del principio de Responsabilidad Única (SRP)
- ❌ Difícil de mantener y testear
- ❌ Acoplamiento alto entre componentes
- ❌ Complejidad cognitiva elevada

---

## ✅ Solución Implementada

### Estructura Nueva

```
apps/core/
├── services.py                    # Orquestación y facade (167 líneas)
└── patterns/                      # Patrones extraídos
    ├── __init__.py               # Exports centralizados
    ├── creational/               # Patrones de creación
    │   ├── __init__.py
    │   └── builder.py            # OrderBuilder
    ├── structural/               # Patrones estructurales
    │   ├── __init__.py
    │   └── adapter.py            # ShippingAdapters + Factory
    └── behavioral/               # Patrones de comportamiento
        ├── __init__.py
        ├── strategy.py           # Estrategias de selección
        └── observer.py           # Sistema de notificaciones
```

---

## 🔧 Patrones de Diseño Implementados

### 1. Builder (Creacional) 📦

**Ubicación:** `patterns/creational/builder.py`

**Responsabilidad:** Construcción compleja de pedidos con validaciones.

**Clase Principal:** `OrderBuilder`

**Uso:**
```python
from .patterns.creational.builder import OrderBuilder

builder = OrderBuilder()
order = (builder
    .with_customer('cliente@email.com')
    .with_address('Calle 123')
    .with_priority('normal')
    .with_fragility('ninguna')
    .with_items({'1': 2, '2': 3})
    .build())
```

**Ventajas:**
- ✅ Validaciones centralizadas (email, dirección)
- ✅ Cálculo automático de peso total
- ✅ Generación de códigos de paquete
- ✅ Interface fluida (method chaining)
- ✅ Estimación de fecha de recogida

---

### 2. Adapter (Estructural) 🔌

**Ubicación:** `patterns/structural/adapter.py`

**Responsabilidad:** Unificar APIs heterogéneas de proveedores de envío.

**Clases Principales:**
- `ShippingProvider` (Protocol/Interface)
- `MotoYAAdapter`
- `EcoBikeAdapter`
- `PaqueteriaZAdapter`
- `ShippingAdapterFactory` (Factory Pattern)

**Uso:**
```python
from .patterns.structural.adapter import ShippingAdapterFactory

# Crear adapter con factory
adapter = ShippingAdapterFactory.create_adapter('motoya')

# Interfaz unificada independiente del proveedor
tracking = adapter.request_pickup({
    'weight': 1500,
    'address': 'Calle 123',
    'priority': 'urgente'
})
```

**Ventajas:**
- ✅ Interfaz común para todos los proveedores
- ✅ Fácil agregar nuevos proveedores (OCP)
- ✅ Encapsula diferencias de APIs externas
- ✅ Testeable con mocks

---

### 3. Strategy (Comportamental) 📊

**Ubicación:** `patterns/behavioral/strategy.py`

**Responsabilidad:** Encapsular algoritmos de selección de proveedor.

**Clases Principales:**
- `ProviderSelectionStrategy` (Abstract Base)
- `StandardSelectionStrategy`
- `EcoFriendlySelectionStrategy`
- `CostOptimizedSelectionStrategy`
- `WeightBasedSelectionStrategy`
- `ProviderSelector` (Context)

**Uso:**
```python
from .patterns.behavioral.strategy import (
    ProviderSelector,
    EcoFriendlySelectionStrategy
)

# Cambiar estrategia en tiempo de ejecución
selector = ProviderSelector(EcoFriendlySelectionStrategy())

provider = selector.select_provider(
    order_data={'weight': 1500, 'priority': 'normal'},
    available_providers=['motoya', 'ecobike', 'paqz']
)
```

**Estrategias Disponibles:**
| Estrategia | Criterio Principal | Uso Recomendado |
|------------|-------------------|-----------------|
| `standard` | Balance de factores | Default del sistema |
| `eco` | Sostenibilidad ambiental | Empresas eco-friendly |
| `cost` | Minimizar costos | Optimización financiera |
| `weight` | Capacidad de peso | Logística simple |

**Ventajas:**
- ✅ Fácil agregar nuevas estrategias
- ✅ Cambio dinámico de algoritmos
- ✅ Testing independiente de cada estrategia
- ✅ Elimina condicionales complejos

---

### 4. Observer (Comportamental) 🔔

**Ubicación:** `patterns/behavioral/observer.py`

**Responsabilidad:** Notificar a múltiples suscriptores de cambios en pedidos.

**Clases Principales:**
- `OrderObserver` (Abstract Base)
- `EmailNotificationObserver`
- `WebhookNotificationObserver`
- `SMSNotificationObserver`
- `LoggingObserver`
- `OrderNotificationSubject` (Subject)

**Uso:**
```python
from .patterns.behavioral.observer import (
    OrderNotificationSubject,
    EmailNotificationObserver,
    WebhookNotificationObserver
)

# Crear sujeto observable
subject = OrderNotificationSubject()

# Adjuntar observadores
subject.attach(EmailNotificationObserver())
subject.attach(WebhookNotificationObserver())

# Notificar a todos
subject.notify({
    'order_code': 'PKG-ABC123',
    'customer_email': 'cliente@email.com',
    'tracking_code': 'MYA-XYZ789'
})
```

**Ventajas:**
- ✅ Desacoplamiento entre pedido y notificaciones
- ✅ Fácil agregar nuevos canales de notificación
- ✅ Notificación automática y consistente
- ✅ Manejo de errores sin afectar otros observadores

---

## 🚀 Uso del Sistema Refactorizado

### Opción 1: Función Principal (Orquestación Completa)

```python
from apps.core.services import handle_create_order

# Todos los patrones se aplican automáticamente
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

### Opción 2: Facade (Interface Simplificada)

```python
from apps.core.services import OrderService

# Crear servicio con estrategia
service = OrderService(strategy_type='cost')

# Crear pedido
order_info = service.create_order(
    customer_email='cliente@email.com',
    address='Calle 123',
    priority='urgente',
    fragility='alta',
    items={'1': 2, '2': 3}
)

# Cambiar estrategia dinámicamente
service.change_strategy('eco')
```

### Opción 3: Uso Directo de Patrones (Máxima Flexibilidad)

```python
from apps.core.patterns import (
    OrderBuilder,
    ShippingAdapterFactory,
    ProviderSelector,
    EcoFriendlySelectionStrategy,
    OrderNotificationSubject
)

# Construir pedido
builder = OrderBuilder()
order = builder.with_customer('test@email.com').with_items({'1': 2}).build()

# Seleccionar proveedor
selector = ProviderSelector(EcoFriendlySelectionStrategy())
provider = selector.select_provider(...)

# Integrar con proveedor
adapter = ShippingAdapterFactory.create_adapter(provider)
tracking = adapter.request_pickup(...)

# Notificar
subject = OrderNotificationSubject()
subject.notify(...)
```

---

## 📊 Comparación Antes vs Después

| Aspecto | Antes (Monolítico) | Después (Limpio) |
|---------|-------------------|------------------|
| **Líneas en services.py** | ~1000 líneas | 167 líneas |
| **Archivos totales** | 1 archivo | 8 archivos |
| **Responsabilidades** | Todo en uno | Separadas por patrón |
| **Testabilidad** | Difícil | Fácil (módulos aislados) |
| **Extensibilidad** | Modificar código existente | Agregar nuevas clases |
| **Principios SOLID** | Violados | Cumplidos |
| **Acoplamiento** | Alto | Bajo |
| **Cohesión** | Baja | Alta |

---

## 🧪 Testing

Cada patrón puede ser testeado independientemente:

```python
# Test Builder
def test_order_builder():
    builder = OrderBuilder()
    order = builder.with_customer('test@test.com').build()
    assert order.customer_email == 'test@test.com'

# Test Strategy
def test_eco_strategy():
    strategy = EcoFriendlySelectionStrategy()
    provider = strategy.select_provider({'weight': 1000}, ['motoya', 'ecobike'])
    assert provider == 'ecobike'

# Test Adapter
def test_adapter_factory():
    adapter = ShippingAdapterFactory.create_adapter('motoya')
    assert adapter.get_provider_name() == 'motoya'

# Test Observer
def test_observer_notification():
    subject = OrderNotificationSubject()
    observer = EmailNotificationObserver()
    subject.attach(observer)
    assert subject.get_observers_count() == 1
```

---

## 🎓 Principios SOLID Aplicados

### 1. **Single Responsibility Principle (SRP)**
- ✅ Cada clase tiene una única razón para cambiar
- ✅ Builder: solo construcción de pedidos
- ✅ Adapter: solo integración con proveedores
- ✅ Strategy: solo selección de proveedor
- ✅ Observer: solo notificaciones

### 2. **Open/Closed Principle (OCP)**
- ✅ Abierto para extensión (agregar nuevas estrategias/adapters)
- ✅ Cerrado para modificación (no cambiar código existente)

### 3. **Liskov Substitution Principle (LSP)**
- ✅ Cualquier estrategia es intercambiable
- ✅ Cualquier adapter es intercambiable

### 4. **Interface Segregation Principle (ISP)**
- ✅ Interfaces específicas (ShippingProvider, OrderObserver)
- ✅ Sin métodos innecesarios

### 5. **Dependency Inversion Principle (DIP)**
- ✅ Depende de abstracciones (Protocols, ABC)
- ✅ No depende de implementaciones concretas

---

## 🔄 Migración desde el Sistema Antiguo

### Paso 1: Actualizar Imports

```python
# Antiguo
from .services import OrderBuilder, ShippingAdapterFactory

# Nuevo
from .patterns.creational.builder import OrderBuilder
from .patterns.structural.adapter import ShippingAdapterFactory
```

### Paso 2: Usar Orquestación Nueva

```python
# Antiguo
order = create_order_old(data)

# Nuevo
from .services import handle_create_order
order_id = handle_create_order(data, strategy_type='standard')
```

---

## 📚 Recursos Adicionales

### Libros Recomendados
- **"Design Patterns"** - Gang of Four
- **"Clean Architecture"** - Robert C. Martin
- **"Refactoring"** - Martin Fowler

### Documentación de Patrones
- Builder: `patterns/creational/builder.py` (docstrings completos)
- Adapter: `patterns/structural/adapter.py` (ejemplos inline)
- Strategy: `patterns/behavioral/strategy.py` (comparativa de algoritmos)
- Observer: `patterns/behavioral/observer.py` (casos de uso)

---

## 🎉 Conclusión

La refactorización ha transformado un sistema monolítico en una **arquitectura limpia y mantenible**:

✅ **Mantenibilidad**: Cada módulo es independiente y fácil de entender  
✅ **Extensibilidad**: Agregar nuevos proveedores/estrategias sin modificar código  
✅ **Testabilidad**: Cada componente puede ser testeado aisladamente  
✅ **Escalabilidad**: Arquitectura preparada para crecimiento  
✅ **Profesionalismo**: Código de nivel productivo con mejores prácticas

---

**Autor:** Refactorización con Arquitectura Limpia  
**Fecha:** 2024  
**Versión:** 1.0  
