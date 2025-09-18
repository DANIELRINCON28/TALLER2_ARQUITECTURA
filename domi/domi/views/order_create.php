<?php /** @var array $products */ $opts = ['ninguna','debil','alta']; ?>
<h1 class="h">Confirmación de Pedido</h1>
<form method="post" action="?r=order/create" class="form">
  <input type="hidden" name="__action" value="order.store">
  <div class="grid2">
    <label class="field"><span>Email del cliente</span><input type="email" name="customer_email" required></label>
    <label class="field"><span>Dirección de entrega</span><input type="text" name="address" required></label>
  </div>
  <div class="grid2">
    <label class="field"><span>Prioridad</span>
      <select name="priority"><option value="normal">Normal</option><option value="express">Express</option></select>
    </label>
    <label class="field"><span>Fragilidad</span>
      <select name="fragility"><?php foreach ($opts as $o): ?><option value="<?= $o ?>"><?= ucfirst($o) ?></option><?php endforeach; ?></select>
    </label>
  </div>
  <h2 class="hh mt">Items</h2>
  <p class="muted">Selecciona cantidades (0 para omitir).</p>
  <?php foreach ($products as $p): ?>
    <label class="field-inline">
      <span><?= htmlspecialchars($p['name']) ?> (<?= (int)$p['weight_grams'] ?> g)</span>
      <input class="qty" type="number" name="items[<?= (int)$p['id'] ?>]" min="0" max="20" value="0">
    </label>
  <?php endforeach; ?>
  <div class="actions mt">
    <button class="btn primary">Confirmar y despachar</button>
    <a class="btn" href="?r=home">Cancelar</a>
  </div>
</form>
<p class="note">Este flujo tiene if/else y funciones directas. El objetivo es **refactorizarlo** aplicando patrones.</p>
