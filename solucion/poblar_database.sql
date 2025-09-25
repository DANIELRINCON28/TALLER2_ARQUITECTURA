-- =====================================================
-- SCRIPT DE POBLACIÓN DE BASE DE DATOS
-- MercadoBarrio - Taller de Patrones de Diseño
-- =====================================================

-- Limpieza previa (opcional)
-- TRUNCATE TABLE notifications RESTART IDENTITY CASCADE;
-- TRUNCATE TABLE shipments RESTART IDENTITY CASCADE;
-- TRUNCATE TABLE order_items RESTART IDENTITY CASCADE;
-- TRUNCATE TABLE orders RESTART IDENTITY CASCADE;
-- TRUNCATE TABLE products RESTART IDENTITY CASCADE;

-- =====================================================
-- TABLA: PRODUCTS
-- =====================================================

INSERT INTO products (sku, name, weight_grams, fragile) VALUES
-- Productos ligeros y no frágiles
('SKU001', 'Arroz Diana 500g', 500, false),
('SKU002', 'Aceite Gourmet 250ml', 300, false),
('SKU003', 'Sal refinada 500g', 500, false),
('SKU004', 'Azúcar blanca 1kg', 1000, false),
('SKU005', 'Pasta Doria 500g', 500, false),

-- Productos medianos
('SKU006', 'Detergente Ariel 1kg', 1100, false),
('SKU007', 'Jabón en polvo 2kg', 2000, false),
('SKU008', 'Champú Sedal 400ml', 450, false),
('SKU009', 'Atún Van Camps 3 latas', 750, false),
('SKU010', 'Leche en polvo Klim 400g', 400, false),

-- Productos pesados
('SKU011', 'Aceite motor 4 litros', 4000, false),
('SKU012', 'Detergente líquido 5L', 5200, false),
('SKU013', 'Bulto arroz 5kg', 5000, false),
('SKU014', 'Caja cerveza 24 unidades', 6000, false),
('SKU015', 'Aceite cocina 1 galón', 3800, false),

-- Productos frágiles ligeros
('SKU016', 'Copas vino cristal (6 und)', 800, true),
('SKU017', 'Platos porcelana (4 und)', 1200, true),
('SKU018', 'Bombillos LED (10 und)', 300, true),
('SKU019', 'Floreros vidrio decorativo', 900, true),
('SKU020', 'Vasos cristal (12 und)', 600, true),

-- Productos frágiles pesados
('SKU021', 'Vajilla completa 50 piezas', 4500, true),
('SKU022', 'Espejo decorativo grande', 3200, true),
('SKU023', 'Lámpara mesa cristal', 2800, true),
('SKU024', 'Set copas champagne (24)', 3600, true),
('SKU025', 'Adornos navideños vidrio', 2200, true),

-- Productos especiales
('SKU026', 'Laptop básica', 1800, true),
('SKU027', 'Microondas pequeño', 8000, false),
('SKU028', 'Cafetera express', 3500, true),
('SKU029', 'Ventilador mesa', 2500, false),
('SKU030', 'Radio portátil bluetooth', 400, true);

-- =====================================================
-- TABLA: ORDERS (Pedidos de ejemplo)
-- =====================================================

INSERT INTO orders (customer_email, address, priority, fragility, total_weight, created_at) VALUES
-- Pedidos normales ligeros
('cliente1@mercadobarrio.com', 'Carrera 15 #93-47, Bogotá', 'normal', 'ninguna', 1300, NOW() - INTERVAL '2 hours'),
('cliente2@mercadobarrio.com', 'Calle 72 #10-34, Medellín', 'normal', 'ninguna', 800, NOW() - INTERVAL '1 hour'),
('cliente3@mercadobarrio.com', 'Avenida Santander #45-67, Cali', 'normal', 'debil', 1500, NOW() - INTERVAL '30 minutes'),

-- Pedidos express frágiles
('cliente4@mercadobarrio.com', 'Transversal 8 #12-90, Barranquilla', 'express', 'alta', 2400, NOW() - INTERVAL '45 minutes'),
('cliente5@mercadobarrio.com', 'Diagonal 25 #34-12, Cartagena', 'express', 'alta', 1800, NOW() - INTERVAL '20 minutes'),

-- Pedidos pesados
('cliente6@mercadobarrio.com', 'Calle Real #67-89, Bucaramanga', 'normal', 'ninguna', 9200, NOW() - INTERVAL '3 hours'),
('cliente7@mercadobarrio.com', 'Avenida Principal #23-45, Pereira', 'normal', 'debil', 7800, NOW() - INTERVAL '1.5 hours'),

-- Pedidos mixtos
('cliente8@mercadobarrio.com', 'Carrera 50 #28-14, Manizales', 'express', 'debil', 3200, NOW() - INTERVAL '10 minutes'),
('cliente9@mercadobarrio.com', 'Calle 80 #15-32, Ibagué', 'normal', 'alta', 4100, NOW() - INTERVAL '25 minutes'),
('cliente10@mercadobarrio.com', 'Avenida Boyacá #45-78, Santa Marta', 'express', 'ninguna', 2800, NOW() - INTERVAL '40 minutes');

-- =====================================================
-- TABLA: ORDER_ITEMS (Items de los pedidos)
-- =====================================================

-- Pedido 1: Productos básicos ligeros (1300g total)
INSERT INTO order_items (order_id, product_id, quantity) VALUES
(1, 1, 2),    -- Arroz 500g x2 = 1000g
(1, 2, 1),    -- Aceite 250ml x1 = 300g
(1, 1, 1);    -- Extra para completar peso

-- Pedido 2: Productos ligeros (800g total)
INSERT INTO order_items (order_id, product_id, quantity) VALUES
(2, 3, 1),    -- Sal 500g
(2, 2, 1);    -- Aceite 300g

-- Pedido 3: Productos medianos (1500g total)
INSERT INTO order_items (order_id, product_id, quantity) VALUES
(3, 6, 1),    -- Detergente 1100g
(3, 8, 1);    -- Champú 450g (frágil débil)

-- Pedido 4: EXPRESS + FRÁGIL (2400g total)
INSERT INTO order_items (order_id, product_id, quantity) VALUES
(4, 16, 2),   -- Copas cristal x2 = 1600g
(4, 17, 1);   -- Platos porcelana = 1200g (frágil alta)

-- Pedido 5: EXPRESS + FRÁGIL ligero (1800g total)
INSERT INTO order_items (order_id, product_id, quantity) VALUES
(5, 26, 1);   -- Laptop = 1800g (frágil alta)

-- Pedido 6: PESADO (9200g total)
INSERT INTO order_items (order_id, product_id, quantity) VALUES
(6, 13, 1),   -- Arroz 5kg = 5000g
(6, 14, 1);   -- Cerveza = 6000g (total > 9kg)

-- Pedido 7: PESADO mediano (7800g total)
INSERT INTO order_items (order_id, product_id, quantity) VALUES
(7, 12, 1),   -- Detergente 5L = 5200g
(8, 15, 1);   -- Aceite galón = 3800g (error intencional para mostrar corrección)

-- Corrección del error anterior
UPDATE order_items SET order_id = 7 WHERE order_id = 8 AND product_id = 15;

-- Pedido 8: EXPRESS + DÉBIL (3200g total)
INSERT INTO order_items (order_id, product_id, quantity) VALUES
(8, 22, 1);   -- Espejo = 3200g (frágil débil)

-- Pedido 9: NORMAL + ALTA fragilidad (4100g total)
INSERT INTO order_items (order_id, product_id, quantity) VALUES
(9, 21, 1);   -- Vajilla completa = 4500g (ajustar peso en update)

-- Ajustar peso del pedido 9
UPDATE orders SET total_weight = 4500 WHERE id = 9;

-- Pedido 10: EXPRESS normal (2800g total)
INSERT INTO order_items (order_id, product_id, quantity) VALUES
(10, 23, 1);  -- Lámpara cristal = 2800g

-- =====================================================
-- TABLA: SHIPMENTS (Envíos de ejemplo)
-- =====================================================

INSERT INTO shipments (order_id, provider, tracking_id, status, created_at) VALUES
-- Pedidos ya confirmados con diferentes estados
(1, 'motoya', 'MYA-ABC123', 'CONFIRMADO', NOW() - INTERVAL '2 hours'),
(2, 'motoya', 'MYA-DEF456', 'DESPACHADO', NOW() - INTERVAL '1 hour'),
(3, 'motoya', 'MYA-GHI789', 'EN_RUTA', NOW() - INTERVAL '30 minutes'),
(4, 'ecobike', 'EBK-JKL012', 'CONFIRMADO', NOW() - INTERVAL '45 minutes'),
(5, 'ecobike', 'EBK-MNO345', 'DESPACHADO', NOW() - INTERVAL '20 minutes'),
(6, 'paqz', 'PAQ-PQR678', 'CONFIRMADO', NOW() - INTERVAL '3 hours'),
(7, 'paqz', 'PAQ-STU901', 'EN_RUTA', NOW() - INTERVAL '1.5 hours'),
(8, 'ecobike', 'EBK-VWX234', 'ENTREGADO', NOW() - INTERVAL '10 minutes'),
(9, 'paqz', 'PAQ-YZA567', 'DESPACHADO', NOW() - INTERVAL '25 minutes'),
(10, 'motoya', 'MYA-BCD890', 'EN_RUTA', NOW() - INTERVAL '40 minutes');

-- =====================================================
-- TABLA: NOTIFICATIONS (Notificaciones de ejemplo)
-- =====================================================

INSERT INTO notifications (order_id, channel, message, created_at) VALUES
-- Notificaciones para pedido 1
(1, 'email', '📧 Pedido #1 confirmado y asignado a motoya (MYA-ABC123)', NOW() - INTERVAL '2 hours'),
(1, 'webhook', '🔗 Webhook: {"order_id":1,"status":"CONFIRMADO","provider":"motoya"}', NOW() - INTERVAL '2 hours'),
(1, 'sms', '📱 Pedido #1 confirmado', NOW() - INTERVAL '2 hours'),

-- Notificaciones para pedido 2 (despachado)
(2, 'email', '📧 Pedido #2 confirmado y asignado a motoya (MYA-DEF456)', NOW() - INTERVAL '1 hour'),
(2, 'webhook', '🔗 Webhook: {"order_id":2,"status":"CONFIRMADO","provider":"motoya"}', NOW() - INTERVAL '1 hour'),
(2, 'email', '📦 Pedido #2 despachado. En preparación para entrega', NOW() - INTERVAL '45 minutes'),
(2, 'sms', '📱 Pedido #2 despachado', NOW() - INTERVAL '45 minutes'),

-- Notificaciones para pedido 3 (en ruta)
(3, 'email', '📧 Pedido #3 confirmado y asignado a motoya (MYA-GHI789)', NOW() - INTERVAL '30 minutes'),
(3, 'webhook', '🔗 Webhook: {"order_id":3,"status":"EN_RUTA","provider":"motoya"}', NOW() - INTERVAL '15 minutes'),
(3, 'sms', '🚚 Pedido #3 en camino', NOW() - INTERVAL '15 minutes'),

-- Notificaciones para pedido 4 (express frágil)
(4, 'email', '📧 Pedido #4 confirmado y asignado a ecobike (EBK-JKL012)', NOW() - INTERVAL '45 minutes'),
(4, 'webhook', '🔗 Webhook: {"order_id":4,"status":"CONFIRMADO","provider":"ecobike","priority":"express"}', NOW() - INTERVAL '45 minutes'),
(4, 'sms', '📱 Pedido #4 confirmado - Express', NOW() - INTERVAL '45 minutes'),

-- Notificaciones para pedido 8 (entregado)
(8, 'email', '📧 Pedido #8 confirmado y asignado a ecobike (EBK-VWX234)', NOW() - INTERVAL '2 hours'),
(8, 'email', '📦 Pedido #8 despachado. Manejo especial para items frágiles', NOW() - INTERVAL '1 hour'),
(8, 'webhook', '🔗 Webhook: {"order_id":8,"status":"EN_RUTA","provider":"ecobike"}', NOW() - INTERVAL '30 minutes'),
(8, 'email', '✅ Pedido #8 entregado exitosamente', NOW() - INTERVAL '10 minutes'),
(8, 'sms', '✅ Pedido #8 entregado', NOW() - INTERVAL '10 minutes');

-- =====================================================
-- VERIFICACIONES Y ESTADÍSTICAS
-- =====================================================

-- Verificar datos insertados
SELECT 'PRODUCTOS' as tabla, COUNT(*) as total FROM products
UNION ALL
SELECT 'PEDIDOS' as tabla, COUNT(*) as total FROM orders
UNION ALL
SELECT 'ITEMS_PEDIDO' as tabla, COUNT(*) as total FROM order_items
UNION ALL
SELECT 'ENVIOS' as tabla, COUNT(*) as total FROM shipments
UNION ALL
SELECT 'NOTIFICACIONES' as tabla, COUNT(*) as total FROM notifications;

-- Resumen por proveedor
SELECT 
    provider as "PROVEEDOR",
    COUNT(*) as "PEDIDOS",
    STRING_AGG(DISTINCT status, ', ') as "ESTADOS"
FROM shipments 
GROUP BY provider 
ORDER BY provider;

-- Resumen por prioridad y fragilidad
SELECT 
    priority as "PRIORIDAD",
    fragility as "FRAGILIDAD", 
    COUNT(*) as "PEDIDOS",
    AVG(total_weight) as "PESO_PROMEDIO"
FROM orders 
GROUP BY priority, fragility 
ORDER BY priority, fragility;

-- =====================================================
-- MENSAJES DE CONFIRMACIÓN
-- =====================================================

SELECT '✅ BASE DE DATOS POBLADA EXITOSAMENTE' as mensaje;
SELECT '📦 30 productos insertados (ligeros, pesados, frágiles)' as detalle;
SELECT '🛒 10 pedidos de ejemplo con diferentes características' as detalle;
SELECT '📋 Items de pedido distribuidos correctamente' as detalle;
SELECT '🚚 10 envíos con diferentes proveedores y estados' as detalle;  
SELECT '🔔 Notificaciones multi-canal para demostración' as detalle;
SELECT '' as mensaje;
SELECT '🚀 LISTO PARA EJECUTAR: python demo_patrones.py' as instruccion;