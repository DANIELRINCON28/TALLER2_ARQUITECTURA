# Contexto para Asistente de Código (GitHub Copilot)

Hola Copilot, este es el contexto para la tarea que vamos a realizar. Por favor, úsalo como guía para tus sugerencias. El objetivo es implementar la funcionalidad "Confirmación de Pedido y Orquestación de Entrega" aplicando tres patrones de diseño (uno creacional, uno estructural y uno de comportamiento).

---

## 1. Contexto del Caso

La empresa **MercadoBarrio** es un marketplace que conecta tiendas de barrio con clientes de la ciudad. Están construyendo su plataforma web y móvil. El foco del sprint actual es el **módulo de Pedidos & Entregas**, que debe:

* Tomar pedidos (carrito → checkout).
* Preparar el despacho (armado del paquete).
* Elegir un **proveedor de entrega** (moto, bicicleta, paquetería).
* **Notificar** al cliente el estado del pedido (creado, despachado, en ruta, entregado).

---

## 2. Objetivo del Ejercicio

Cada equipo debe implementar **una funcionalidad específica** aplicando **tres patrones de diseño** (uno por cada familia: creacional, estructural y de comportamiento). La elección del patrón es libre dentro de cada familia, justificando por qué es el más adecuado para el problema.

---

## 3. Funcionalidad a Implementar (Scope Acotado)

### "Confirmación de Pedido y Orquestación de Entrega"

**Flujo resumido:**

1.  El cliente confirma el pedido (con ítems, dirección y medio de pago ya validados).
2.  El sistema **construye** un objeto `Pedido` listo para despachar (aplicando reglas de empaquetado/fragilidad).
3.  El sistema **elige** un proveedor de entrega apropiado (según ciudad, costo, tiempo, restricciones).
4.  El sistema **adapta o compone** la integración con el proveedor externo (cuyas APIs son heterogéneas) para solicitar el retiro.
5.  El sistema **notifica** al cliente los cambios de estado (pedido confirmado → despachado → en ruta → entregado).

**Entregable técnico mínimo:** Endpoints/controlador o un script ejecutable que dispare este flujo, mostrando **logs claros** y una **salida visible** (consola, JSON o una interfaz web simple).

---

## 4. Requisitos Funcionales (RF)

* **RF1. Confirmar pedido:**
    * `idCliente`: `string`
    * `items[]`: `Array<{sku: string, nombre: string, cantidad: number}>`
    * `direccionEntrega`: `string`
    * `prioridad`: `'normal' | 'express'`
    * `fragilidad`: `'ninguna' | 'débil' | 'alta'`

* **RF2. Construir objeto `Pedido` para despacho:**
    * Debe agregar los siguientes atributos:
        * `codigoPaquete`: `string` (generado)
        * `pesoEstimado`: `number` (calculado)
        * `etiquetaManejo`: `string` (ej. "FRÁGIL", si aplica)
        * `fechaRecogidaEstimada`: `Date`

* **RF3. Seleccionar proveedor de entrega:**
    * Proveedores disponibles: `MotoYA`, `EcoBike`, `PaqueteríaZ`.
    * **Política de selección:**
        1.  Si está dentro del radio urbano y el pedido es liviano → preferir **MotoYA**.
        2.  Si la prioridad es `express` y es frágil → priorizar **EcoBike** si está disponible.
        3.  Si está fuera del radio urbano o es muy pesado → usar **PaqueteríaZ**.

* **RF4. Integrar con el proveedor:**
    * Llamar a la API del proveedor elegido para solicitar la recogida.
    * Obtener y almacenar un `trackingId` de la respuesta.

* **RF5. Registrar y notificar estados:**
    * El pedido debe transicionar por los estados: `CONFIRMADO`, `DESPACHADO`, `EN_RUTA`, `ENTREGADO`.
    * Se debe notificar al cliente en cada cambio de estado.

* **RF6. Persistencia:**
    * No es obligatoria. Se puede simular con una estructura de datos en memoria o archivos JSON.

---

## 5. Requisitos No Funcionales (RNF)

* **RNF1. Calidad del código:**
    * Modular y legible.
    * Bajo acoplamiento y alta cohesión.

* **RNF2. Extensibilidad:**
    * Debe ser fácil sustituir o añadir nuevos proveedores de entrega sin modificar el flujo principal (respetando principios como OCP/DIP).

* **RNF3. Trazabilidad:**
    * Usar logs para registrar decisiones clave del flujo, como el patrón de diseño utilizado y el proveedor seleccionado.