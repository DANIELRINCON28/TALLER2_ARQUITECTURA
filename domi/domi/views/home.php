<?php /** @var array $products */ /** @var array $recent */ ?>
<h1 class="h">Módulo de Pedidos & Entregas (Starter)</h1>
<p class="muted">Código base **sin patrones de diseño**. La tarea es refactorizar aplicando uno creacional, uno estructural y uno de comportamiento.</p>

<h2 class="hh">Productos</h2>
<ul class="list">
<?php foreach ($products as $p): ?>
  <li class="list-item"><strong><?= htmlspecialchars($p['name']) ?></strong> <span class="muted">(<?= (int)$p['weight_grams'] ?> g)</span></li>
<?php endforeach; ?>
</ul>

<h2 class="hh">Pedidos recientes</h2>
<?php if (empty($recent)): ?>
  <p class="muted">Aún no hay pedidos.</p>
<?php else: ?>
  <ul class="list">
  <?php foreach ($recent as $o): ?>
    <li class="list-item">
      <span>#<?= (int)$o['id'] ?> • <?= htmlspecialchars($o['customer_email']) ?> • <?= htmlspecialchars($o['priority']) ?> • peso <?= (int)$o['total_weight'] ?> g</span>
      <a class="chip" href="?r=order/show&id=<?= (int)$o['id'] ?>">ver</a>
    </li>
  <?php endforeach; ?>
  </ul>
<?php endif; ?>

<div class="actions mt"><a class="btn primary" href="?r=order/create">➕ Crear nuevo pedido</a></div>
