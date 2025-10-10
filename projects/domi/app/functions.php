<?php
// Estado del proyecto hasta el requerimiento: lógica directa sin patrones de diseño.
// NOTA: el objetivo del taller es refactorizar este código para introducir patrones (creacional, estructural, comportamiento).

function products_all(): array {
  return db()->query("SELECT * FROM products ORDER BY name ASC")->fetchAll();
}

function orders_latest(int $limit=5): array {
  $stmt = db()->query("SELECT * FROM orders ORDER BY id DESC LIMIT " . (int)$limit);
  return $stmt->fetchAll();
}

function order_with_items(int $id): ?array {
  $stmt = db()->prepare("SELECT * FROM orders WHERE id=?");
  $stmt->execute([$id]);
  $order = $stmt->fetch();
  if (!$order) return null;
  $stmt = db()->prepare("SELECT oi.*, p.name FROM order_items oi JOIN products p ON p.id=oi.product_id WHERE order_id=?");
  $stmt->execute([$id]);
  $items = $stmt->fetchAll();
  return ['order'=>$order, 'items'=>$items];
}

function shipment_by_order(int $orderId): ?array {
  $stmt = db()->prepare("SELECT * FROM shipments WHERE order_id=? ORDER BY id DESC LIMIT 1");
  $stmt->execute([$orderId]);
  $r = $stmt->fetch();
  return $r ?: null;
}

function handle_create_order(array $input): int {
  $email = filter_var(trim((string)($input['customer_email'] ?? '')), FILTER_VALIDATE_EMAIL);
  $address = trim((string)($input['address'] ?? ''));
  $priority = (string)($input['priority'] ?? 'normal');
  $fragility = (string)($input['fragility'] ?? 'ninguna');
  $items = $input['items'] ?? [];

  if (!$email) throw new RuntimeException('Email inválido');
  if ($address === '') throw new RuntimeException('Dirección requerida');

  // Resolver items y calcular peso total (lógica directa, ideal para aplicar Builder luego)
  $pdo = db();
  $pdo->beginTransaction();
  try {
    $totalWeight = 0;
    $resolved = [];
    $stmt = $pdo->prepare("SELECT id, weight_grams FROM products WHERE id=?");
    foreach ($items as $productId => $qty) {
      $qty = (int)$qty;
      if ($qty <= 0) continue;
      $stmt->execute([$productId]);
      $row = $stmt->fetch();
      if (!$row) continue;
      $totalWeight += ((int)$row['weight_grams'] * $qty);
      $resolved[] = ['product_id'=>(int)$row['id'], 'quantity'=>$qty];
    }
    if (empty($resolved)) throw new RuntimeException('El pedido no tiene items válidos');

    // Insertar pedido
    $stmt = $pdo->prepare("INSERT INTO orders (customer_email,address,priority,fragility,total_weight) VALUES (?,?,?,?,?)");
    $stmt->execute([$email, $address, $priority, $fragility, $totalWeight]);
    $orderId = (int)$pdo->lastInsertId();

    // Insertar items
    $stmtItem = $pdo->prepare("INSERT INTO order_items (order_id,product_id,quantity) VALUES (?,?,?)");
    foreach ($resolved as $it) {
      $stmtItem->execute([$orderId, $it['product_id'], $it['quantity']]);
    }

    // Selección de proveedor con if/else (ideal para Strategy luego)
    $provider = select_provider_naive($priority, $fragility, $totalWeight);

    // Simulación de “integración” (ideal para Adapter luego)
    $tracking = request_pickup_naive($provider, ['order_id'=>$orderId, 'weight'=>$totalWeight]);

    // Registrar envío
    $stmt = $pdo->prepare("INSERT INTO shipments (order_id,provider,tracking_id,status) VALUES (?,?,?,?)");
    $stmt->execute([$orderId, $provider, $tracking, 'CONFIRMADO']);

    // Notificación directa (ideal para Observer luego)
    $msg = "Pedido #$orderId confirmado y asignado a $provider ($tracking)";
    $stmt = $pdo->prepare("INSERT INTO notifications (order_id,channel,message) VALUES (?,?,?)");
    $stmt->execute([$orderId,'email',$msg]);
    $stmt->execute([$orderId,'webhook',$msg]);

    $pdo->commit();
    return $orderId;
  } catch (Throwable $e) {
    $pdo->rollBack();
    throw $e;
  }
}

function select_provider_naive(string $priority, string $fragility, int $totalWeight): string {
  if ($priority === 'express' && $fragility !== 'ninguna') {
    return 'ecobike';
  }
  if ($totalWeight <= 1200) {
    return 'motoya';
  }
  return 'paqz';
}

function request_pickup_naive(string $provider, array $data): string {
  // Simula distintas formas de generar tracking por proveedor (sin interfaces comunes)
  if ($provider === 'motoya') {
    return 'MYA-' . strtoupper(bin2hex(random_bytes(3)));
  } elseif ($provider === 'ecobike') {
    return 'EBK-' . strtoupper(bin2hex(random_bytes(3)));
  } else {
    return 'PAQ-' . strtoupper(bin2hex(random_bytes(3)));
  }
}
