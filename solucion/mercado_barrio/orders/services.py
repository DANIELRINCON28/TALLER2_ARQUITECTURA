"""
Funciones de negocio para la aplicación de pedidos.
Traducción directa de functions.php manteniendo la misma lógica de negocio.
Estado del proyecto hasta el requerimiento: lógica directa sin patrones de diseño.
NOTA: el objetivo del taller es refactorizar este código para introducir patrones (creacional, estructural, comportamiento).
"""
import secrets
from typing import List, Dict, Optional, Any
from django.db import transaction
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Product, Order, OrderItem, Shipment, Notification


def products_all() -> List[Product]:
    """
    Obtiene todos los productos ordenados por nombre.
    Traducción directa de: products_all() en functions.php
    Equivalente a: SELECT * FROM products ORDER BY name ASC
    """
    return list(Product.objects.all().order_by('name'))


def orders_latest(limit: int = 5) -> List[Order]:
    """
    Obtiene los últimos pedidos limitados por cantidad.
    Traducción directa de: orders_latest(int $limit=5) en functions.php
    Equivalente a: SELECT * FROM orders ORDER BY id DESC LIMIT {limit}
    """
    return list(Order.objects.all().order_by('-id')[:limit])


def order_with_items(order_id: int) -> Optional[Dict[str, Any]]:
    """
    Obtiene un pedido con sus items asociados.
    Traducción directa de: order_with_items(int $id) en functions.php
    
    Args:
        order_id: ID del pedido a buscar
        
    Returns:
        Diccionario con 'order' y 'items' o None si no existe
    """
    try:
        # Equivalente a: SELECT * FROM orders WHERE id=?
        order = Order.objects.get(id=order_id)
        
        # Equivalente a: SELECT oi.*, p.name FROM order_items oi JOIN products p ON p.id=oi.product_id WHERE order_id=?
        items = OrderItem.objects.filter(order_id=order_id).select_related('product')
        
        return {
            'order': order,
            'items': list(items)
        }
    except Order.DoesNotExist:
        return None


def shipment_by_order(order_id: int) -> Optional[Shipment]:
    """
    Obtiene el envío más reciente para un pedido.
    Traducción directa de: shipment_by_order(int $orderId) en functions.php
    Equivalente a: SELECT * FROM shipments WHERE order_id=? ORDER BY id DESC LIMIT 1
    """
    try:
        return Shipment.objects.filter(order_id=order_id).order_by('-id').first()
    except Shipment.DoesNotExist:
        return None


def handle_create_order(input_data: Dict[str, Any]) -> int:
    """
    Maneja la creación completa de un pedido.
    Traducción directa de: handle_create_order(array $input) en functions.php
    Mantiene la misma lógica de validación, cálculo de peso, selección de proveedor y notificaciones.
    
    Args:
        input_data: Diccionario con datos del formulario
        
    Returns:
        ID del pedido creado
        
    Raises:
        ValueError: Si los datos de entrada no son válidos
    """
    # Validación de email - equivalente a filter_var(trim(...), FILTER_VALIDATE_EMAIL)
    email = input_data.get('customer_email', '').strip()
    try:
        validate_email(email)
    except ValidationError:
        raise ValueError('Email inválido')
    
    # Validación de dirección
    address = input_data.get('address', '').strip()
    if not address:
        raise ValueError('Dirección requerida')
    
    # Obtener otros campos
    priority = input_data.get('priority', 'normal')
    fragility = input_data.get('fragility', 'ninguna')
    items = input_data.get('items', {})
    
    # Resolver items y calcular peso total (lógica directa, ideal para aplicar Builder luego)
    with transaction.atomic():  # Equivalente a $pdo->beginTransaction()
        try:
            total_weight = 0
            resolved_items = []
            
            # Procesar cada item del pedido
            for product_id, qty in items.items():
                qty = int(qty)
                if qty <= 0:
                    continue
                    
                try:
                    # Equivalente a: SELECT id, weight_grams FROM products WHERE id=?
                    product = Product.objects.get(id=product_id)
                    total_weight += (product.weight_grams * qty)
                    resolved_items.append({
                        'product_id': product.id,
                        'quantity': qty
                    })
                except Product.DoesNotExist:
                    continue
            
            if not resolved_items:
                raise ValueError('El pedido no tiene items válidos')
            
            # Insertar pedido - equivalente a INSERT INTO orders
            order = Order.objects.create(
                customer_email=email,
                address=address,
                priority=priority,
                fragility=fragility,
                total_weight=total_weight
            )
            
            # Insertar items - equivalente a INSERT INTO order_items
            for item in resolved_items:
                OrderItem.objects.create(
                    order_id=order.id,
                    product_id=item['product_id'],
                    quantity=item['quantity']
                )
            
            # Selección de proveedor con if/else (ideal para Strategy luego)
            provider = select_provider_naive(priority, fragility, total_weight)
            
            # Simulación de "integración" (ideal para Adapter luego)
            tracking = request_pickup_naive(provider, {
                'order_id': order.id,
                'weight': total_weight
            })
            
            # Registrar envío - equivalente a INSERT INTO shipments
            Shipment.objects.create(
                order=order,
                provider=provider,
                tracking_id=tracking,
                status='CONFIRMADO'
            )
            
            # Notificación directa (ideal para Observer luego)
            message = f"Pedido #{order.id} confirmado y asignado a {provider} ({tracking})"
            
            # Equivalente a INSERT INTO notifications para email y webhook
            Notification.objects.create(
                order=order,
                channel='email',
                message=message
            )
            Notification.objects.create(
                order=order,
                channel='webhook',
                message=message
            )
            
            return order.id
            
        except Exception as e:
            # El transaction.atomic() maneja automáticamente el rollback
            raise e


def select_provider_naive(priority: str, fragility: str, total_weight: int) -> str:
    """
    Selecciona proveedor de envío usando lógica simple con if/else.
    Traducción directa de: select_provider_naive(...) en functions.php
    Esta lógica es ideal para refactorizar usando el patrón Strategy.
    
    Args:
        priority: Prioridad del envío ('normal' o 'express')
        fragility: Nivel de fragilidad ('ninguna', 'debil', 'alta')
        total_weight: Peso total en gramos
        
    Returns:
        Nombre del proveedor seleccionado
    """
    if priority == 'express' and fragility != 'ninguna':
        return 'ecobike'
    if total_weight <= 1200:
        return 'motoya'
    return 'paqz'


def request_pickup_naive(provider: str, data: Dict[str, Any]) -> str:
    """
    Simula distintas formas de generar tracking por proveedor.
    Traducción directa de: request_pickup_naive(...) en functions.php
    Sin interfaces comunes - ideal para refactorizar usando el patrón Adapter.
    
    Args:
        provider: Nombre del proveedor
        data: Datos del pedido
        
    Returns:
        Código de tracking generado
    """
    # Simula distintas formas de generar tracking por proveedor (sin interfaces comunes)
    if provider == 'motoya':
        return f'MYA-{secrets.token_hex(3).upper()}'
    elif provider == 'ecobike':
        return f'EBK-{secrets.token_hex(3).upper()}'
    else:
        return f'PAQ-{secrets.token_hex(3).upper()}'