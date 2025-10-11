from typing import List, Dict, Optional, Any
from django.db import transaction
from .models import Product, Order, OrderItem, Shipment, Notification

from .patterns.creacional.builder import OrderBuilder

from .patterns.estructural.adapter import ShippingAdapterFactory

from .patterns.comportamental.strategy import (
    ProviderSelector,
    StandardSelectionStrategy,
    get_strategy_by_name
)

from .patterns.comportamental.observer import (
    OrderNotificationSubject,
    create_default_observers
)

def products_all() -> List[Product]:
    """Obtiene todos los productos ordenados por nombre."""
    return list(Product.objects.all().order_by('name'))

def orders_latest(limit: int = 5) -> List[Order]:
    """Obtiene los últimos pedidos."""
    return list(Order.objects.all().order_by('-id')[:limit])

def order_with_items(order_id: int) -> Optional[Dict[str, Any]]:
    """Obtiene un pedido con sus items."""
    try:
        order = Order.objects.get(id=order_id)
        items = OrderItem.objects.filter(order_id=order_id).select_related('product')
        return {'order': order, 'items': list(items)}
    except Order.DoesNotExist:
        return None

def shipment_by_order(order_id: int) -> Optional[Shipment]:
    """Obtiene el envío de un pedido."""
    return Shipment.objects.filter(order_id=order_id).order_by('-id').first()

def handle_create_order(input_data: Dict[str, Any], strategy_type: str = 'standard') -> int:
    """
    Crea un pedido usando TODOS los patrones de diseño.
    
    Args:
        input_data: Datos del pedido
        strategy_type: Estrategia de selección ('standard' | 'eco' | 'cost')
    
    Returns:
        ID del pedido creado
    """
    print(" Iniciando creación con patrones")
    
    # BUILDER: Construir pedido
    builder = OrderBuilder()
    order = (builder
            .with_customer(input_data.get('customer_email', ''))
            .with_address(input_data.get('address', ''))
            .with_priority(input_data.get('priority', 'normal'))
            .with_fragility(input_data.get('fragility', 'ninguna'))
            .with_items(input_data.get('items', {}))
            .build())
    
    order_summary = builder.get_order_summary()
    print(f" Pedido #{order.id} construido")
    
    # STRATEGY: Seleccionar proveedor
    try:
        strategy = get_strategy_by_name(strategy_type)
    except ValueError:
        strategy = StandardSelectionStrategy()
    
    selector = ProviderSelector(strategy)
    selection_data = {
        'priority': order.priority,
        'fragility': order.fragility,
        'weight': order.total_weight,
        'address': order.address
    }
    available_providers = ShippingAdapterFactory.get_available_providers()
    selected_provider = selector.select_provider(selection_data, available_providers)
    print(f" Proveedor: {selected_provider}")
    
    # ADAPTER: Integrar con proveedor
    provider_adapter = ShippingAdapterFactory.create_adapter(selected_provider)
    adapter_data = {
        'order_id': order.id,
        'weight': order.total_weight,
        'priority': order.priority,
        'fragility': order.fragility,
        'address': order.address
    }
    tracking_code = provider_adapter.request_pickup(adapter_data)
    print(f" Tracking: {tracking_code}")
    
    # Registrar envío
    with transaction.atomic():
        Shipment.objects.create(
            order=order,
            provider=selected_provider,
            tracking_id=tracking_code,
            status='CONFIRMADO'
        )
    
    # OBSERVER: Notificar
    notification_subject = OrderNotificationSubject()
    observers = create_default_observers()
    for observer in observers:
        notification_subject.attach(observer)
    
    notification_data = {
        'order_code': order_summary['package_code'],
        'customer_email': order.customer_email,
        'tracking_code': tracking_code,
        'provider_name': selected_provider,
        'pickup_date': order_summary['estimated_pickup_date'],
        'weight': order.total_weight,
        'priority': order.priority,
        'fragility': order.fragility,
        'address': order.address
    }
    notification_subject.notify(notification_data)
    print(f" Notificaciones enviadas")
    
    return order.id

def get_order_processing_info(order_id: int) -> Dict[str, Any]:
    """
    Obtiene información detallada sobre los patrones aplicados en un pedido.
    Útil para auditoría y documentación del sistema.
    
    Args:
        order_id: ID del pedido
        
    Returns:
        Diccionario con información de patrones aplicados
    """
    try:
        order = Order.objects.get(id=order_id)
        shipment = Shipment.objects.filter(order_id=order_id).first()
        notifications = Notification.objects.filter(order_id=order_id)
        
        return {
            'order_id': order_id,
            'patterns_applied': {
                'builder': {
                    'name': 'Builder (Creacional)',
                    'purpose': 'Construcción compleja del pedido',
                    'evidence': {
                        'package_code': f'PKG-{order.id:08X}',
                        'weight_calculated': f'{order.total_weight}g',
                        'validations_passed': True
                    }
                },
                'strategy': {
                    'name': 'Strategy (Comportamental)',
                    'purpose': 'Selección inteligente de proveedor',
                    'evidence': {
                        'provider_selected': shipment.provider if shipment else 'N/A',
                        'factors': f'Peso: {order.total_weight}g, Prioridad: {order.priority}, Fragilidad: {order.fragility}'
                    }
                },
                'adapter': {
                    'name': 'Adapter (Eestructural)',
                    'purpose': 'Integración uniforme con APIs',
                    'evidence': {
                        'provider_integrated': shipment.provider if shipment else 'N/A',
                        'tracking_generated': shipment.tracking_id if shipment else 'N/A',
                        'unified_interface_used': True
                    }
                },
                'observer': {
                    'name': 'Observer (Comportamental)',
                    'purpose': 'Notificaciones multi-canal',
                    'evidence': {
                        'notifications_sent': notifications.count(),
                        'channels': list(notifications.values_list('channel', flat=True).distinct())
                    }
                }
            },
            'architecture_benefits': {
                'maintainability': 'Cada patrón en su propio módulo (SRP)',
                'extensibility': 'Fácil agregar nuevos proveedores/estrategias (OCP)',
                'testability': 'Patrones aislados facilitan testing unitario',
                'readability': 'Responsabilidades claras y documentadas'
            }
        }
        
    except Order.DoesNotExist:
        raise ValueError(f'Pedido #{order_id} no encontrado')
class OrderService:
    """Facade para operaciones de pedidos."""
    
    def __init__(self, strategy_type: str = 'standard'):
        self.strategy_type = strategy_type
    
    def create_order(self, customer_email: str, address: str, priority: str, 
                    fragility: str, items: Dict[str, int]) -> Dict[str, Any]:
        """Crea un pedido completo."""
        input_data = {
            'customer_email': customer_email,
            'address': address,
            'priority': priority,
            'fragility': fragility,
            'items': items
        }
        order_id = handle_create_order(input_data, self.strategy_type)
        return self.get_order_info(order_id)
    
    def get_order_info(self, order_id: int) -> Dict[str, Any]:
        """Obtiene información del pedido."""
        try:
            order = Order.objects.get(id=order_id)
            shipment = Shipment.objects.filter(order_id=order_id).first()
            return {
                'order_id': order.id,
                'customer_email': order.customer_email,
                'provider': shipment.provider if shipment else None,
                'tracking_id': shipment.tracking_id if shipment else None
            }
        except Order.DoesNotExist:
            raise ValueError(f'Pedido #{order_id} no encontrado')
