# Patrones de Diseño - Sistema de Pedidos

Este directorio contiene la implementación de patrones de diseño para el sistema de gestión de pedidos, siguiendo principios de arquitectura limpia.

## 📁 Estructura

```
patterns/
├── __init__.py                 # Exports centralizados
├── creational/                 # Patrones de Creación
│   ├── __init__.py
│   └── builder.py             # Builder Pattern
├── structural/                 # Patrones Estructurales
│   ├── __init__.py
│   └── adapter.py             # Adapter Pattern + Factory
└── behavioral/                 # Patrones de Comportamiento
    ├── __init__.py
    ├── strategy.py            # Strategy Pattern
    └── observer.py            # Observer Pattern
```

## 🎨 Patrones Implementados

### 1. Builder (Creacional)

**Archivo:** `creational/builder.py`  
**Clase:** `OrderBuilder`

Construye objetos complejos paso a paso, separando la construcción de la representación.

```python
from apps.core.patterns.creational.builder import OrderBuilder

order = (OrderBuilder()
    .with_customer('cliente@email.com')
    .with_address('Calle 123')
    .with_priority('urgente')
    .with_items({'1': 2, '3': 1})
    .build())
```

**Responsabilidades:**
- ✅ Validar email y dirección
- ✅ Calcular peso total del pedido
- ✅ Generar código de paquete único
- ✅ Determinar etiqueta de manejo
- ✅ Estimar fecha de recogida

---

### 2. Adapter (Estructural)

**Archivo:** `structural/adapter.py`  
**Clases:** `ShippingAdapterFactory`, `MotoYAAdapter`, `EcoBikeAdapter`, `PaqueteriaZAdapter`

Convierte la interfaz de una clase en otra que los clientes esperan.

```python
from apps.core.patterns.structural.adapter import ShippingAdapterFactory

# Factory crea el adapter apropiado
adapter = ShippingAdapterFactory.create_adapter('motoya')

# Interfaz unificada para todos los proveedores
tracking = adapter.request_pickup({
    'weight': 1500,
    'address': 'Calle Principal 456',
    'priority': 'normal'
})
```

**Proveedores Adaptados:**
- 🚴 **MotoYA**: Entregas rápidas en moto
- 🚲 **EcoBike**: Entregas ecológicas en bicicleta
- 📦 **PaqueteríaZ**: Paquetería tradicional

**Responsabilidades:**
- ✅ Interfaz común `ShippingProvider`
- ✅ Adaptación de APIs heterogéneas
- ✅ Factory para creación centralizada
- ✅ Extensibilidad para nuevos proveedores

---

### 3. Strategy (Comportamental)

**Archivo:** `behavioral/strategy.py`  
**Clase:** `ProviderSelector` + Estrategias concretas

Define una familia de algoritmos, encapsula cada uno y los hace intercambiables.

```python
from apps.core.patterns.behavioral.strategy import (
    ProviderSelector,
    EcoFriendlySelectionStrategy
)

# Selector con estrategia ecológica
selector = ProviderSelector(EcoFriendlySelectionStrategy())

provider = selector.select_provider(
    order_data={'weight': 1000, 'fragility': 'alta'},
    available_providers=['motoya', 'ecobike', 'paqz']
)
```

**Estrategias Disponibles:**
| Estrategia | Criterio | Cuando Usar |
|------------|----------|-------------|
| `StandardSelectionStrategy` | Balance de factores | Default del sistema |
| `EcoFriendlySelectionStrategy` | Sostenibilidad | Compromiso ambiental |
| `CostOptimizedSelectionStrategy` | Minimizar costos | Optimización financiera |
| `WeightBasedSelectionStrategy` | Capacidad | Logística simple |

**Responsabilidades:**
- ✅ Encapsular algoritmos de selección
- ✅ Cambio dinámico de estrategias
- ✅ Fácil agregar nuevas estrategias
- ✅ Eliminar condicionales complejos

---

### 4. Observer (Comportamental)

**Archivo:** `behavioral/observer.py`  
**Clase:** `OrderNotificationSubject` + Observadores

Define una dependencia uno-a-muchos para notificar cambios automáticamente.

```python
from apps.core.patterns.behavioral.observer import (
    OrderNotificationSubject,
    EmailNotificationObserver,
    SMSNotificationObserver,
    create_default_observers
)

# Crear sujeto observable
subject = OrderNotificationSubject()

# Adjuntar observadores
for observer in create_default_observers():
    subject.attach(observer)

# Notificar a todos
subject.notify({
    'order_code': 'PKG-ABC123',
    'customer_email': 'cliente@email.com',
    'tracking_code': 'MYA-XYZ789'
})
```

**Observadores Implementados:**
- 📧 **EmailNotificationObserver**: Notificaciones por correo
- 🔗 **WebhookNotificationObserver**: Integración con sistemas externos
- 📱 **SMSNotificationObserver**: Alertas SMS para urgentes
- 📝 **LoggingObserver**: Registro en logs del sistema

**Responsabilidades:**
- ✅ Notificación automática multi-canal
- ✅ Desacoplamiento entre pedido y notificaciones
- ✅ Fácil agregar nuevos canales
- ✅ Manejo de errores sin afectar otros observadores

---

## 🚀 Uso Rápido

### Import Centralizado

Todos los patrones están disponibles desde el módulo raíz:

```python
from apps.core.patterns import (
    # Builder
    OrderBuilder,
    
    # Adapter
    ShippingAdapterFactory,
    
    # Strategy
    ProviderSelector,
    StandardSelectionStrategy,
    EcoFriendlySelectionStrategy,
    
    # Observer
    OrderNotificationSubject,
    create_default_observers
)
```

### Uso Individual de Patrones

```python
# Builder: Construir pedido
builder = OrderBuilder()
order = builder.with_customer('test@test.com').with_items({'1': 2}).build()

# Strategy: Seleccionar proveedor
selector = ProviderSelector(EcoFriendlySelectionStrategy())
provider = selector.select_provider(order_data, ['motoya', 'ecobike'])

# Adapter: Integrar con proveedor
adapter = ShippingAdapterFactory.create_adapter(provider)
tracking = adapter.request_pickup(order_data)

# Observer: Notificar
subject = OrderNotificationSubject()
subject.attach(EmailNotificationObserver())
subject.notify(notification_data)
```

---

## 🧪 Testing

Cada patrón es testeable independientemente:

```python
# Test unitario del Builder
def test_builder_validates_email():
    builder = OrderBuilder()
    with pytest.raises(ValueError):
        builder.with_customer('invalid-email')

# Test unitario del Strategy
def test_eco_strategy_selects_ecobike():
    strategy = EcoFriendlySelectionStrategy()
    provider = strategy.select_provider(
        {'weight': 1000}, 
        ['motoya', 'ecobike']
    )
    assert provider == 'ecobike'

# Test unitario del Adapter
def test_adapter_factory():
    adapter = ShippingAdapterFactory.create_adapter('motoya')
    assert adapter.get_provider_name() == 'motoya'

# Test unitario del Observer
def test_observer_count():
    subject = OrderNotificationSubject()
    subject.attach(EmailNotificationObserver())
    assert subject.get_observers_count() == 1
```

---

## 📋 Principios SOLID

Todos los patrones siguen principios SOLID:

### Single Responsibility (SRP)
✅ Cada clase tiene una única responsabilidad

### Open/Closed (OCP)
✅ Abierto para extensión, cerrado para modificación

### Liskov Substitution (LSP)
✅ Subtipos son intercambiables

### Interface Segregation (ISP)
✅ Interfaces específicas y pequeñas

### Dependency Inversion (DIP)
✅ Depende de abstracciones, no de concreciones

---

## 🔧 Extensibilidad

### Agregar Nueva Estrategia

```python
# En behavioral/strategy.py
class CustomSelectionStrategy(ProviderSelectionStrategy):
    def select_provider(self, order_data, available_providers):
        # Tu algoritmo personalizado
        return selected_provider
```

### Agregar Nuevo Proveedor

```python
# En structural/adapter.py
class CustomProviderAdapter:
    def __init__(self):
        self._provider = CustomProvider()
    
    def request_pickup(self, order_data):
        # Adaptar API del proveedor
        return tracking_code
    
    def get_provider_name(self):
        return 'custom'

# Registrar en factory
ShippingAdapterFactory.register_provider('custom', CustomProviderAdapter)
```

### Agregar Nuevo Observador

```python
# En behavioral/observer.py
class CustomNotificationObserver(OrderObserver):
    def update(self, order_data):
        # Tu lógica de notificación
        pass
```

---

## 📚 Referencias

- **Gang of Four (GoF)**: Design Patterns - Elements of Reusable Object-Oriented Software
- **Robert C. Martin**: Clean Architecture
- **Martin Fowler**: Refactoring

---

## ✨ Ventajas de Esta Arquitectura

1. **Mantenibilidad**: Código organizado y fácil de entender
2. **Testabilidad**: Cada componente es testeable aisladamente
3. **Extensibilidad**: Agregar funcionalidad sin modificar código existente
4. **Reusabilidad**: Patrones reutilizables en otros contextos
5. **Escalabilidad**: Arquitectura preparada para crecimiento
6. **Profesionalismo**: Código de nivel empresarial

---

**Documentación completa:** `docs/ARQUITECTURA_PATRONES.md`
