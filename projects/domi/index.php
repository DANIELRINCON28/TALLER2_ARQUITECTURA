<?php
declare(strict_types=1);
session_start();
require_once __DIR__ . '/config.php';
require_once __DIR__ . '/app/db.php';
require_once __DIR__ . '/app/functions.php';

if (APP_DEBUG) { ini_set('display_errors','1'); ini_set('display_startup_errors','1'); error_reporting(E_ALL); }

function view(string $name, array $params = []) {
  extract($params);
  include __DIR__ . '/views/layout.php';
}

$route = $_GET['r'] ?? 'home';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  $action = $_POST['__action'] ?? '';
  try {
    if ($action === 'order.store') {
      $orderId = handle_create_order($_POST);
      $_SESSION['flash'] = ['type'=>'success','msg'=>"Pedido confirmado (#$orderId)"];
      header("Location: ?r=order/show&id=".$orderId); exit;
    }
  } catch (Throwable $e) {
    $_SESSION['flash'] = ['type'=>'danger','msg'=>$e->getMessage()];
    $route = 'order/create';
  }
}

switch ($route) {
  case 'home':
    $products = products_all();
    $recent   = orders_latest(5);
    view('home', compact('products','recent'));
    break;
  case 'order/create':
    $products = products_all();
    view('order_create', compact('products'));
    break;
  case 'order/show':
    $id = (int)($_GET['id'] ?? 0);
    $order = order_with_items($id);
    $shipment = shipment_by_order($id);
    view('order_show', compact('order','shipment'));
    break;
  default:
    http_response_code(404);
    echo "<h1>404</h1><p>Ruta no encontrada.</p>";
}
