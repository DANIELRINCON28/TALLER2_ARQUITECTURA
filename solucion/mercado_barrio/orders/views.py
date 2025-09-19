"""
Vistas para la aplicación de pedidos.
Traducción directa del sistema de routing en index.php manteniendo la misma lógica.
Equivalente al switch/case para manejar las diferentes rutas (?r=home, ?r=order/create, etc.)
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from .services import (
    products_all, 
    orders_latest, 
    order_with_items, 
    shipment_by_order, 
    handle_create_order
)


def home_view(request):
    """
    Vista principal - equivalente a case 'home' en index.php.
    Muestra productos y pedidos recientes.
    """
    # Equivalente a: $products = products_all();
    products = products_all()
    
    # Equivalente a: $recent = orders_latest(5);
    recent = orders_latest(5)
    
    # Equivalente a: view('home', compact('products','recent'));
    context = {
        'products': products,
        'recent': recent
    }
    
    return render(request, 'orders/home.html', context)


@require_http_methods(["GET", "POST"])
@csrf_protect
def order_create_view(request):
    """
    Vista para crear pedidos - equivalente a case 'order/create' en index.php.
    Maneja tanto GET (mostrar formulario) como POST (procesar pedido).
    """
    if request.method == 'POST':
        # Equivalente al manejo de $_POST en index.php
        action = request.POST.get('__action', '')
        
        if action == 'order.store':
            try:
                # Preparar datos del formulario - equivalente a $_POST en PHP
                form_data = {
                    'customer_email': request.POST.get('customer_email', ''),
                    'address': request.POST.get('address', ''),
                    'priority': request.POST.get('priority', 'normal'),
                    'fragility': request.POST.get('fragility', 'ninguna'),
                    'items': {}
                }
                
                # Procesar items del formulario
                for key, value in request.POST.items():
                    if key.startswith('items[') and key.endswith(']'):
                        # Extraer product_id de items[123] 
                        product_id = key[6:-1]  # Remover 'items[' y ']'
                        try:
                            form_data['items'][int(product_id)] = int(value)
                        except (ValueError, TypeError):
                            continue
                
                # Equivalente a: $orderId = handle_create_order($_POST);
                order_id = handle_create_order(form_data)
                
                # Equivalente a: $_SESSION['flash'] = ['type'=>'success','msg'=>"Pedido confirmado (#$orderId)"];
                messages.success(request, f"Pedido confirmado (#{order_id})")
                
                # Equivalente a: header("Location: ?r=order/show&id=".$orderId);
                return redirect('order_show', order_id=order_id)
                
            except Exception as e:
                # Equivalente a: $_SESSION['flash'] = ['type'=>'danger','msg'=>$e->getMessage()];
                messages.error(request, str(e))
                # Continúa ejecutando el GET para mostrar el formulario nuevamente
    
    # Mostrar formulario (GET) - equivalente a: $products = products_all();
    products = products_all()
    
    # Equivalente a: view('order_create', compact('products'));
    context = {
        'products': products,
        'fragility_options': ['ninguna', 'debil', 'alta']  # Equivalente a $opts en PHP
    }
    
    return render(request, 'orders/order_create.html', context)


def order_show_view(request, order_id):
    """
    Vista para mostrar detalles de pedido - equivalente a case 'order/show' en index.php.
    
    Args:
        order_id: ID del pedido a mostrar - equivalente a $_GET['id'] en PHP
    """
    # Equivalente a: $id = (int)($_GET['id'] ?? 0);
    try:
        order_id = int(order_id)
    except (ValueError, TypeError):
        order_id = 0
    
    # Equivalente a: $order = order_with_items($id);
    order_data = order_with_items(order_id)
    
    # Equivalente a: $shipment = shipment_by_order($id);
    shipment = shipment_by_order(order_id)
    
    # Equivalente a: view('order_show', compact('order','shipment'));
    context = {
        'order': order_data,
        'shipment': shipment
    }
    
    return render(request, 'orders/order_show.html', context)