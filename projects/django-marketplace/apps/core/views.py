"""
Vistas para la aplicación de pedidos con PATRONES DE DISEÑO implementados.
Integra Builder, Adapter, Strategy y Observer según las directrices del proyecto.

Patrones implementados:
- CREACIONAL: Builder - Para construcción compleja de pedidos
- Eestructural: Adapter - Para integración con proveedores de entrega
- COMPORTAMENTAL: Strategy - Para selección inteligente de proveedores
- COMPORTAMENTAL: Observer - Para sistema de notificaciones multi-canal
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from .services import (
    products_all, 
    orders_latest, 
    order_with_items, 
    shipment_by_order, 
    handle_create_order,
    # Importar servicios con patrones de diseño
    OrderService,
    get_order_processing_info
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
    Vista para crear pedidos usando TODOS LOS PATRONES DE DISEÑO.
    
    Flujo implementado:
    1. BUILDER: Construcción compleja del pedido con validaciones
    2. STRATEGY: Selección inteligente del proveedor de entrega
    3. ADAPTER: Integración unificada con API del proveedor
    4. OBSERVER: Notificaciones multi-canal automáticas
    """
    if request.method == 'POST':
        action = request.POST.get('__action', '')
        
        if action == 'order.store':
            try:
                # Preparar datos del formulario según directrices
                form_data = {
                    'customer_email': request.POST.get('customer_email', ''),
                    'address': request.POST.get('address', ''),
                    'priority': request.POST.get('priority', 'normal'),  # 'normal' | 'express'
                    'fragility': request.POST.get('fragility', 'ninguna'),  # 'ninguna' | 'debil' | 'alta'
                    'items': {},
                    'strategy': request.POST.get('strategy', 'standard')  # Estrategia de selección
                }
                
                # Procesar items del formulario
                for key, value in request.POST.items():
                    if key.startswith('items[') and key.endswith(']'):
                        product_id = key[6:-1]
                        try:
                            quantity = int(value)
                            if quantity > 0:  # Solo agregar items con cantidad > 0
                                form_data['items'][int(product_id)] = quantity
                        except (ValueError, TypeError):
                            continue
                
                # USAR SERVICIO CON PATRONES DE DISEÑO
                order_service = OrderService()
                order_result = order_service.create_order_with_patterns(
                    customer_email=form_data['customer_email'],
                    address=form_data['address'],
                    priority=form_data['priority'],
                    fragility=form_data['fragility'],
                    items=form_data['items'],
                    strategy=form_data['strategy']
                )
                
                # Mensaje de éxito con información de patrones
                success_msg = (
                    f"✅ Pedido #{order_result['order_id']} creado exitosamente con patrones de diseño!\n"
                    f"🔨 Builder: {order_result['patterns_used']['builder']}\n"
                    f"📊 Strategy: {order_result['patterns_used']['strategy']}\n"
                    f"🔌 Adapter: {order_result['patterns_used']['adapter']}\n"
                    f"🔔 Observer: {order_result['patterns_used']['observer']}"
                )
                messages.success(request, success_msg)
                
                return redirect('order_show', order_id=order_result['order_id'])
                
            except Exception as e:
                messages.error(request, f"❌ Error al crear pedido: {str(e)}")
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
    Vista para mostrar detalles de pedido con información de PATRONES DE DISEÑO.
    
    Muestra:
    - Información del pedido construido con Builder
    - Detalles del proveedor seleccionado con Strategy
    - Integración realizada con Adapter
    - Historial de notificaciones del Observer
    
    Args:
        order_id: ID del pedido a mostrar
    """
    try:
        order_id = int(order_id)
    except (ValueError, TypeError):
        order_id = 0
    
    # Obtener datos básicos del pedido
    order_data = order_with_items(order_id)
    shipment = shipment_by_order(order_id)
    
    # Obtener información detallada de patrones de diseño
    patterns_info = get_order_processing_info(order_id)
    
    context = {
        'order': order_data,
        'shipment': shipment,
        'patterns_info': patterns_info,  # Información adicional de patrones
    }
    
    return render(request, 'orders/order_show.html', context)


def order_status_api(request, order_id):
    """
    API para obtener estado del pedido en tiempo real.
    Útil para demostrar el patrón Observer en acción.
    """
    try:
        order_id = int(order_id)
        order_service = OrderService()
        
        # Simular cambio de estado para demostrar Observer
        if request.method == 'POST':
            new_status = request.POST.get('status', 'dispatched')
            notifications_sent = order_service.simulate_status_change(order_id, new_status)
            
            return JsonResponse({
                'success': True,
                'status_changed': new_status,
                'notifications_sent': notifications_sent,
                'pattern_used': 'Observer - Sistema de notificaciones automáticas'
            })
        
        # GET: Obtener estado actual
        status_info = order_service.get_order_status(order_id)
        return JsonResponse(status_info)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)