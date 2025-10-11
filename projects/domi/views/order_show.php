<?php /** @var array|null $order */ /** @var array|null $shipment */ ?>
<?php if (!$order): ?>
  <p class="muted">Pedido no encontrado.</p>
<?php else: $o=$order['order']; ?>
<h1 class="h">Pedido #<?= (int)$o['id'] ?></h1>
<p><strong>Cliente:</strong> <?= htmlspecialchars($o['customer_email']) ?> • <strong>Dirección:</strong> <?= htmlspecialchars($o['address']) ?></p>
<p><strong>Prioridad:</strong> <?= htmlspecialchars($o['priority']) ?> • <strong>Fragilidad:</strong> <?= htmlspecialchars($o['fragility']) ?> • <strong>Peso total:</strong> <?= (int)$o['total_weight'] ?> g</p>

<h2 class="hh">Items</h2>
<ul class="list">
<?php foreach ($order['items'] as $it): ?>
  <li class="list-item"><?= htmlspecialchars($it['name']) ?> × <?= (int)$it['quantity'] ?></li>
<?php endforeach; ?>
</ul>

<h2 class="hh">Envío</h2>
<?php if (!$shipment): ?>
  <p class="muted">Envío no registrado.</p>
<?php else: ?>
  <p><strong>Proveedor:</strong> <?= htmlspecialchars($shipment['provider']) ?> • <strong>Tracking:</strong> <?= htmlspecialchars($shipment['tracking_id']) ?> • <strong>Estado:</strong> <?= htmlspecialchars($shipment['status']) ?></p>
<?php endif; ?>

<p class="note">Revisa la tabla <code>notifications</code> para ver los “mensajes enviados” (simulados).</p>
<?php endif; ?>
