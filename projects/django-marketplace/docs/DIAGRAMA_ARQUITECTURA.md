# Diagrama de Arquitectura - Sistema de Patrones de Diseño

## 🏗️ Arquitectura General

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                            │
│                     (views.py, templates)                       │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FACADE / SERVICE LAYER                       │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │             services.py (167 líneas)                       │ │
│  │                                                            │ │
│  │  • products_all()                                         │ │
│  │  • orders_latest()                                        │ │
│  │  • handle_create_order()  ← Orquestación principal       │ │
│  │  • OrderService (Facade)                                  │ │
│  └────────────────────────────────────────────────────────────┘ │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PATTERNS LAYER                              │
│                  (Patrones de Diseño)                            │
│                                                                  │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐      │
│  │  CREATIONAL   │  │  STRUCTURAL   │  │  BEHAVIORAL   │      │
│  ├───────────────┤  ├───────────────┤  ├───────────────┤      │
│  │               │  │               │  │               │      │
│  │   Builder     │  │   Adapter     │  │   Strategy    │      │
│  │               │  │               │  │   Observer    │      │
│  └───────────────┘  └───────────────┘  └───────────────┘      │
│                                                                  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                       DATA LAYER                                 │
│                    (models.py - Django ORM)                      │
│                                                                  │
│  • Product  • Order  • OrderItem  • Shipment  • Notification    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Flujo de Creación de Pedido

```
    Usuario
      │
      │ POST /orders/create/
      ▼
┌──────────────────┐
│   views.py       │
│  order_create()  │
└────────┬─────────┘
         │
         │ input_data
         ▼
┌──────────────────────────────────────┐
│     services.py                      │
│  handle_create_order(input_data)    │
└────────┬─────────────────────────────┘
         │
         │ PASO 1: BUILDER
         ▼
┌────────────────────────────┐
│  patterns/creational/      │
│     builder.py             │
│                            │
│  OrderBuilder()            │
│    .with_customer()        │
│    .with_address()         │
│    .with_items()           │
│    .build() ──────────┐    │
│                       │    │
└───────────────────────┼────┘
                        │ Order object
         ┌──────────────┘
         │
         │ PASO 2: STRATEGY
         ▼
┌────────────────────────────────┐
│  patterns/behavioral/          │
│     strategy.py                │
│                                │
│  ProviderSelector              │
│  ┌──────────────────────────┐  │
│  │ StandardSelectionStrategy│  │
│  │ EcoFriendlyStrategy      │  │
│  │ CostOptimizedStrategy    │  │
│  └──────────┬───────────────┘  │
│             │                  │
└─────────────┼──────────────────┘
              │ selected_provider
              │
              │ PASO 3: ADAPTER
              ▼
┌─────────────────────────────────────┐
│  patterns/structural/               │
│     adapter.py                      │
│                                     │
│  ShippingAdapterFactory             │
│    .create_adapter(provider)        │
│                                     │
│  ┌──────┐  ┌──────┐  ┌──────┐      │
│  │MotoYA│  │EcoBike│ │PaqZ  │      │
│  │Adapter│  │Adapter│ │Adapter│     │
│  └───┬──┘  └───┬──┘  └───┬──┘      │
│      │         │         │          │
└──────┼─────────┼─────────┼──────────┘
       │         │         │
       └─────────┴─────────┘
                 │ tracking_code
                 │
                 │ PASO 4: OBSERVER
                 ▼
┌──────────────────────────────────────┐
│  patterns/behavioral/                │
│     observer.py                      │
│                                      │
│  OrderNotificationSubject            │
│    .attach(observers)                │
│    .notify(order_data)               │
│                                      │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌────┐ │
│  │Email │ │Webhook│ │SMS   │ │Log │ │
│  │Observer│Observer│Observer│Observer│
│  └──────┘ └──────┘ └──────┘ └────┘ │
│     │        │        │        │    │
└─────┼────────┼────────┼────────┼────┘
      │        │        │        │
      ▼        ▼        ▼        ▼
   [📧]     [🔗]     [📱]     [📝]
   Email   Webhook   SMS      Logs
```

---

## 📦 Patrón Builder - Detalle

```
OrderBuilder
    │
    ├─ with_customer(email)
    │   └─ validate_email()
    │       └─ Django's validate_email()
    │
    ├─ with_address(address)
    │   └─ strip() & validate not empty
    │
    ├─ with_priority(priority)
    │   └─ 'normal' | 'urgente'
    │
    ├─ with_fragility(fragility)
    │   └─ 'ninguna' | 'media' | 'alta'
    │
    ├─ with_items(items_dict)
    │   ├─ Product.objects.get(id)
    │   ├─ Calculate weight per item
    │   └─ Sum total weight
    │
    └─ build()
        ├─ _generate_package_code()
        │   └─ "PKG-{hex(6).upper()}"
        │
        ├─ _determine_handling_label()
        │   └─ Based on fragility
        │
        ├─ _estimate_pickup_date()
        │   └─ now() + hours offset
        │
        └─ Order.objects.create()
            └─ OrderItem.objects.create() (loop)
```

---

## 🔌 Patrón Adapter - Detalle

```
ShippingAdapterFactory
    │
    └─ create_adapter(provider_name)
        │
        ├─ 'motoya' ──────► MotoYAAdapter
        │                      │
        │                      └─ MotoYAProvider (API Externa)
        │                          └─ create_delivery_request()
        │                              └─ return "MYA-{hex(3)}"
        │
        ├─ 'ecobike' ─────► EcoBikeAdapter
        │                      │
        │                      └─ EcoBikeProvider (API Externa)
        │                          └─ schedule_pickup()
        │                              └─ return "EBK-{hex(3)}"
        │
        └─ 'paqz' ────────► PaqueteriaZAdapter
                               │
                               └─ PaqueteriaZProvider (API Externa)
                                   └─ submit_shipment()
                                       └─ return "PAQ-{hex(3)}"

Todos implementan: ShippingProvider (Protocol)
    ├─ request_pickup(order_data) → str
    └─ get_provider_name() → str
```

---

## 📊 Patrón Strategy - Detalle

```
ProviderSelector (Context)
    │
    ├─ strategy: ProviderSelectionStrategy
    │
    └─ select_provider(order_data, providers)
        │
        └─ strategy.select_provider()
            │
            ├─ StandardSelectionStrategy
            │   ├─ IF fragility != 'ninguna' AND priority != 'urgente'
            │   │   → ecobike
            │   ├─ IF weight > 5000g
            │   │   → paqz
            │   ├─ IF priority == 'urgente'
            │   │   → motoya
            │   └─ DEFAULT
            │       → motoya
            │
            ├─ EcoFriendlySelectionStrategy
            │   ├─ PRIORITY 1: ecobike
            │   │   (IF weight <= 10kg AND priority != 'urgente')
            │   ├─ PRIORITY 2: motoya
            │   └─ PRIORITY 3: paqz
            │
            ├─ CostOptimizedSelectionStrategy
            │   ├─ Calculate cost for each provider
            │   │   └─ cost = base + (per_kg * weight)
            │   └─ SELECT cheapest
            │
            └─ WeightBasedSelectionStrategy
                ├─ IF weight < 2kg → ecobike
                ├─ IF weight 2-8kg → motoya
                └─ IF weight > 8kg → paqz
```

---

## 🔔 Patrón Observer - Detalle

```
OrderNotificationSubject
    │
    ├─ _observers: List[OrderObserver]
    │
    ├─ attach(observer)
    │   └─ _observers.append(observer)
    │
    ├─ detach(observer)
    │   └─ _observers.remove(observer)
    │
    └─ notify(order_data)
        │
        └─ FOR EACH observer IN _observers:
            │
            ├─ EmailNotificationObserver
            │   └─ update(order_data)
            │       └─ send_email(to, subject, body)
            │
            ├─ WebhookNotificationObserver
            │   └─ update(order_data)
            │       └─ requests.post(webhook_url, json=payload)
            │
            ├─ SMSNotificationObserver
            │   └─ update(order_data)
            │       └─ IF priority == 'urgente':
            │           └─ send_sms(phone, message)
            │
            └─ LoggingObserver
                └─ update(order_data)
                    └─ logger.info(order_details)
```

---

## 🎯 Principios SOLID en la Arquitectura

```
┌────────────────────────────────────────────────────────┐
│  SINGLE RESPONSIBILITY PRINCIPLE (SRP)                 │
├────────────────────────────────────────────────────────┤
│  OrderBuilder        → Solo construcción de pedidos    │
│  ShippingAdapter     → Solo integración con proveedores│
│  ProviderSelector    → Solo selección de proveedor     │
│  OrderObserver       → Solo notificaciones             │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│  OPEN/CLOSED PRINCIPLE (OCP)                           │
├────────────────────────────────────────────────────────┤
│  ✅ Agregar nueva estrategia sin modificar selector    │
│  ✅ Agregar nuevo adapter sin modificar factory        │
│  ✅ Agregar nuevo observer sin modificar subject       │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│  LISKOV SUBSTITUTION PRINCIPLE (LSP)                   │
├────────────────────────────────────────────────────────┤
│  ✅ Cualquier Strategy es intercambiable               │
│  ✅ Cualquier Adapter es intercambiable                │
│  ✅ Cualquier Observer es intercambiable               │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│  INTERFACE SEGREGATION PRINCIPLE (ISP)                 │
├────────────────────────────────────────────────────────┤
│  ✅ ShippingProvider: solo request_pickup()            │
│  ✅ OrderObserver: solo update()                       │
│  ✅ Interfaces específicas y pequeñas                  │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│  DEPENDENCY INVERSION PRINCIPLE (DIP)                  │
├────────────────────────────────────────────────────────┤
│  ✅ Depende de Protocol/ABC (abstracciones)            │
│  ✅ No depende de implementaciones concretas           │
│  ✅ Inyección de dependencias vía constructor          │
└────────────────────────────────────────────────────────┘
```

---

## 📈 Beneficios de la Arquitectura

```
ANTES (Monolítico)              DESPUÉS (Limpio)
═══════════════════             ═══════════════════
┌─────────────────┐             ┌─────────┬─────────┬─────────┐
│  services.py    │             │ Builder │ Adapter │Strategy │
│  (1000 líneas)  │             │         │         │         │
│                 │    ───►     ├─────────┴─────────┴─────────┤
│ Todo en uno     │             │      Observer               │
│ • Builder       │             ├─────────────────────────────┤
│ • Adapter       │             │   services.py (167 líneas)  │
│ • Strategy      │             │   Orquestación              │
│ • Observer      │             └─────────────────────────────┘
│ • Utils         │
│ • Legacy        │             ✅ Mantenible
└─────────────────┘             ✅ Testeable
                                ✅ Extensible
❌ Difícil mantener              ✅ Escalable
❌ Acoplado                      ✅ SOLID
❌ No testeable
```

---

**Documentación completa:** `docs/ARQUITECTURA_PATRONES.md`  
**README de patrones:** `apps/core/patterns/README.md`
