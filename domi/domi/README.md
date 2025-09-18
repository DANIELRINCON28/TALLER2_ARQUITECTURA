# Starter PHP + MySQL (sin patrones) — MercadoBarrio
Este es el **estado del proyecto justo antes del requerimiento**. No hay patrones implementados. La lógica es directa y está lista para **refactorizar** aplicando: 1 creacional, 1 estructural y 1 de comportamiento.

## Requisitos
- XAMPP (PHP 8+, MySQL) — Ajusta `config.php` si es necesario.

## Instalación
1. Copia la carpeta a `C:\xampp\htdocs\cine-patterns-starter-plain\`
2. Importa la base de datos (en consola o phpMyAdmin):
   - `db/schema.sql`
   - `db/seed.sql`
3. Abre `http://localhost/cine-patterns-starter-plain/`

## Flujo incluido
- Página de **Confirmación de Pedido** (formulario).
- Al enviar, el código:
  - Valida email/dirección.
  - Resuelve items y **calcula peso total**.
  - Inserta en `orders` y `order_items`.
  - **Selecciona proveedor con if/else** (naive).
  - Genera **tracking simulado** con funciones directas (sin interfaces).
  - Inserta en `shipments` y una “notificación” en `notifications`.
- Página de **Detalle de Pedido** con envío y items.
- Página de **Inicio** con productos y últimos pedidos.

## Tarea (para estudiantes)
- Refactorizar introduciendo:
  - **1 patrón creacional** (p. ej., Builder para construir el pedido),
  - **1 patrón estructural** (p. ej., Adapter para unificar proveedores),
  - **1 patrón de comportamiento** (p. ej., Strategy para elección de proveedor u Observer para notificaciones).
- Dejar comentarios `// [Patrón: ...]` donde lo apliquen y explicar en el README (breve).

¡Éxitos!