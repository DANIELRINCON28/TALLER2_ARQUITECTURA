# Actividad — TALLER2_ARQUITECTURA

## 1) Contexto
La empresa **MercadoBarrio** es un marketplace que conecta tiendas de barrio con clientes de la ciudad. Están construyendo su plataforma web y móvil. El foco del sprint actual es el módulo **Pedidos & Entregas**, que debe:

- Tomar pedidos (carrito → checkout)
- Preparar el despacho (armado del paquete)
- Elegir un proveedor de entrega (moto, bicicleta, paquetería)
- Notificar al cliente el estado del pedido (creado → despachado → en ruta → entregado)

---

## 2) Objetivo del ejercicio
Cada equipo debe implementar una funcionalidad específica aplicando tres patrones (uno por familia). La elección del patrón es libre dentro de cada familia y debe justificarse por qué ese patrón es el más adecuado.

**Funcionalidad a implementar (scope acotado):**

> Confirmación de Pedido y Orquestación de Entrega

---

## 3) Flujo resumido

1. El cliente confirma el pedido (con items, dirección y medio de pago ya validados).
2. El sistema construye un objeto `Pedido` listo para despachar (aplica reglas de empaquetado/fragilidad).
3. El sistema elige un proveedor de entrega apropiado según ciudad, costo, tiempo y restricciones.
4. El sistema adapta o compone la integración con el proveedor externo (APIs heterogéneas) para solicitar el retiro.
5. El sistema notifica al cliente los cambios de estado (CONFIRMADO → DESPACHADO → EN_RUTA → ENTREGADO).

---

## 4) Requisitos funcionales

- RF1 — Confirmar pedido con: `idCliente`, `items[]` (sku, nombre, cantidad), `direccionEntrega`, `prioridad` (normal/express), `fragilidad` (ninguna/débil/alta).

- RF2 — Construir un objeto `Pedido` listo para despacho, agregando: código de paquete, peso estimado, etiqueta de manejo (si frágil), fecha/hora de recogida estimada.

- RF3 — Seleccionar proveedor de entrega entre: `MotoYA`, `EcoBike`, `PaqueteríaZ` con la siguiente política:
  - Dentro del radio urbano y pedido liviano → preferir `MotoYA`.
  - Si `prioridad == express` y `fragilidad == alta` → priorizar `EcoBike` si está disponible.
  - Si fuera de rango o muy pesado → `PaqueteríaZ`.

- RF4 — Integrar con el proveedor elegido para solicitar la recogida y obtener un `trackingId`.

- RF5 — Registrar y notificar al cliente los estados: `CONFIRMADO`, `DESPACHADO`, `EN_RUTA`, `ENTREGADO`.

- RF6 — Persistencia no obligatoria: se puede simular con in-memory o archivos.

---

## Requisitos no funcionales (RNF)

- RNF1 — Código modular y legible, con bajo acoplamiento y alta cohesión.
- RNF2 — Facilitar sustitución de proveedores sin romper el flujo (OCP/DIP).
- RNF3 — Trazabilidad por logs (identificar patrón usado y decisiones).

---

## Entregable técnico mínimo

- Endpoints / controlador o script ejecutable que dispare el flujo con logs claros y salida visible (consola, JSON o web simple).

---

## Sugerencias de implementación

- Diseña un objeto `Pedido` y un `OrderBuilder` (si aplicas patrón Builder).
- Usa Strategy/Factory para seleccionar el proveedor de entrega.
- Implementa un adaptador (Adapter) para cada proveedor externo.
- Registra eventos y estados (Observer o Publisher-Subscriber) para notificaciones y logs.

---

## Criterios de evaluación

- Correcta separación de responsabilidades (controladores, servicios, modelos, templates).
- Uso coherente de patrones de diseño y justificación de su elección.
- Código limpio, testeable y con logs que permitan trazar decisiones.
- Entregable ejecutable que demuestre el flujo descrito.
