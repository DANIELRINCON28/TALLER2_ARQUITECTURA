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

def handle_create_order(input_data: Dict[str, Any], strategy_type: str = 'standard', pattern_logs: Dict[str, list] = None) -> int:
    """
    Crea un pedido usando TODOS los patrones de diseño.
    
    Args:
        input_data: Datos del pedido
        strategy_type: Estrategia de selección ('standard' | 'eco' | 'cost')
        pattern_logs: Diccionario para registrar logs detallados de cada patrón
    
    Returns:
        ID del pedido creado
    """
    if pattern_logs is None:
        pattern_logs = {'builder': [], 'strategy': [], 'adapter': [], 'observer': []}
    
    print(" Iniciando creación con patrones")
    
    # BUILDER: Construir pedido
    pattern_logs['builder'].append("🔨 PATRÓN BUILDER INICIADO")
    pattern_logs['builder'].append(f"Cliente: {input_data.get('customer_email', '')}")
    pattern_logs['builder'].append(f"Dirección: {input_data.get('address', '')}")
    pattern_logs['builder'].append(f"Prioridad: {input_data.get('priority', 'normal')}")
    pattern_logs['builder'].append(f"Fragilidad: {input_data.get('fragility', 'ninguna')}")
    
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
    
    pattern_logs['builder'].append(f"✓ Pedido #{order.id} construido exitosamente")
    pattern_logs['builder'].append(f"Código paquete: {order_summary['package_code']}")
    pattern_logs['builder'].append(f"Peso total calculado: {order.total_weight}g")
    pattern_logs['builder'].append(f"Etiqueta de manejo: {order_summary['handling_label']}")
    pattern_logs['builder'].append(f"Fecha estimada: {order_summary['estimated_pickup_date']}")
    
    # STRATEGY: Seleccionar proveedor
    pattern_logs['strategy'].append("📊 PATRÓN STRATEGY INICIADO")
    try:
        strategy = get_strategy_by_name(strategy_type)
        pattern_logs['strategy'].append(f"Estrategia seleccionada: {strategy_type.upper()}")
    except ValueError:
        strategy = StandardSelectionStrategy()
        pattern_logs['strategy'].append(f"Estrategia por defecto: STANDARD")
    
    selector = ProviderSelector(strategy)
    selection_data = {
        'priority': order.priority,
        'fragility': order.fragility,
        'weight': order.total_weight,
        'address': order.address
    }
    pattern_logs['strategy'].append(f"Factores de decisión:")
    pattern_logs['strategy'].append(f"  - Prioridad: {selection_data['priority']}")
    pattern_logs['strategy'].append(f"  - Fragilidad: {selection_data['fragility']}")
    pattern_logs['strategy'].append(f"  - Peso: {selection_data['weight']}g")
    pattern_logs['strategy'].append(f"  - Dirección: {selection_data['address']}")
    
    available_providers = ShippingAdapterFactory.get_available_providers()
    pattern_logs['strategy'].append(f"Proveedores disponibles: {', '.join(available_providers)}")
    
    selected_provider = selector.select_provider(selection_data, available_providers)
    print(f" Proveedor: {selected_provider}")
    
    pattern_logs['strategy'].append(f"✓ Proveedor seleccionado: {selected_provider.upper()}")
    pattern_logs['strategy'].append(f"Razón: {strategy.__class__.__name__} aplicó su algoritmo")
    
    # ADAPTER: Integrar con proveedor
    pattern_logs['adapter'].append("🔌 PATRÓN ADAPTER INICIADO")
    pattern_logs['adapter'].append(f"Creando adaptador para: {selected_provider}")
    
    provider_adapter = ShippingAdapterFactory.create_adapter(selected_provider)
    pattern_logs['adapter'].append(f"Adaptador creado: {provider_adapter.__class__.__name__}")
    pattern_logs['adapter'].append(f"Interfaz unificada: ShippingProviderInterface")
    
    adapter_data = {
        'order_id': order.id,
        'weight': order.total_weight,
        'priority': order.priority,
        'fragility': order.fragility,
        'address': order.address
    }
    pattern_logs['adapter'].append(f"Datos enviados al proveedor:")
    pattern_logs['adapter'].append(f"  - Order ID: {adapter_data['order_id']}")
    pattern_logs['adapter'].append(f"  - Weight: {adapter_data['weight']}g")
    pattern_logs['adapter'].append(f"  - Priority: {adapter_data['priority']}")
    
    tracking_code = provider_adapter.request_pickup(adapter_data)
    print(f" Tracking: {tracking_code}")
    
    pattern_logs['adapter'].append(f"✓ Tracking code generado: {tracking_code}")
    pattern_logs['adapter'].append(f"Proveedor nombre: {provider_adapter.get_provider_name()}")
    
    # Registrar envío
    with transaction.atomic():
        Shipment.objects.create(
            order=order,
            provider=selected_provider,
            tracking_id=tracking_code,
            status='CONFIRMADO'
        )
    pattern_logs['adapter'].append(f"✓ Envío registrado en base de datos")
    
    # OBSERVER: Notificar
    pattern_logs['observer'].append("🔔 PATRÓN OBSERVER INICIADO")
    pattern_logs['observer'].append("Creando subject y registrando observers...")
    
    notification_subject = OrderNotificationSubject()
    observers = create_default_observers()
    
    observer_names = []
    for observer in observers:
        notification_subject.attach(observer)
        observer_name = observer.__class__.__name__
        observer_names.append(observer_name)
        pattern_logs['observer'].append(f"  - Observer registrado: {observer_name}")
    
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
    
    pattern_logs['observer'].append(f"Notificando a {len(observers)} observers...")
    notification_subject.notify(notification_data)
    print(f" Notificaciones enviadas")
    
    # Contar notificaciones en BD
    notifications_count = Notification.objects.filter(order_id=order.id).count()
    pattern_logs['observer'].append(f"✓ {notifications_count} notificaciones enviadas y guardadas en BD")
    
    channels = Notification.objects.filter(order_id=order.id).values_list('channel', flat=True).distinct()
    pattern_logs['observer'].append(f"Canales utilizados: {', '.join(channels)}")
    
    return order.id

class OrderService:
    """Facade para operaciones de pedidos."""
    
    def __init__(self, strategy_type: str = 'standard'):
        self.strategy_type = strategy_type
    
 
    def create_order_with_patterns(self, customer_email: str, address: str, priority: str, 
                                   fragility: str, items: Dict[str, int], 
                                   strategy: str = 'standard') -> Dict[str, Any]:
        """
        Crea un pedido usando todos los patrones de diseño.
        
        Returns:
            Diccionario con order_id, detalles del pedido y logs detallados
        """
        pattern_logs = {
            'builder': [],
            'strategy': [],
            'adapter': [],
            'observer': []
        }
        
        input_data = {
            'customer_email': customer_email,
            'address': address,
            'priority': priority,
            'fragility': fragility,
            'items': items
        }
        
        # Registrar inicio
        pattern_logs['builder'].append(f"Iniciando construcción de pedido para {customer_email}")
        
        order_id = handle_create_order(input_data, strategy, pattern_logs)
        
        # Obtener información de patrones aplicados
        order_info = self.get_order_info(order_id)
        
        return {
            'order_id': order_id,
            'success': True,
            'patterns_used': order_info['patterns_used'],
            'pattern_logs': pattern_logs
        }
    
    def get_order_info(self, order_id: int) -> Dict[str, Any]:
        """Obtiene información del pedido con detalles de patrones aplicados."""
        try:
            order = Order.objects.get(id=order_id)
            shipment = Shipment.objects.filter(order_id=order_id).first()
            notifications = Notification.objects.filter(order_id=order_id)
            
            return {
                'order_id': order.id,
                'customer_email': order.customer_email,
                'provider': shipment.provider if shipment else None,
                'tracking_id': shipment.tracking_id if shipment else None,
                'patterns_used': {
                    'builder': f'Pedido PKG-{order.id:08X} construido con peso {order.total_weight}g',
                    'strategy': f'Proveedor {shipment.provider if shipment else "N/A"} seleccionado',
                    'adapter': f'Tracking {shipment.tracking_id if shipment else "N/A"} generado',
                    'observer': f'{notifications.count()} notificaciones enviadas'
                }
            }
        except Order.DoesNotExist:
            raise ValueError(f'Pedido #{order_id} no encontrado')
    
    def get_order_status(self, order_id: int) -> Dict[str, Any]:
        """Obtiene el estado actual del pedido."""
        try:
            order = Order.objects.get(id=order_id)
            shipment = Shipment.objects.filter(order_id=order_id).first()
            
            return {
                'order_id': order.id,
                'status': shipment.status if shipment else 'PENDING',
                'tracking_id': shipment.tracking_id if shipment else None,
                'provider': shipment.provider if shipment else None
            }
        except Order.DoesNotExist:
            raise ValueError(f'Pedido #{order_id} no encontrado')
    
    def simulate_status_change(self, order_id: int, new_status: str, observer_logs: list = None) -> list:
        """Simula cambio de estado y dispara notificaciones Observer."""
        if observer_logs is None:
            observer_logs = []
            
        try:
            order = Order.objects.get(id=order_id)
            shipment = Shipment.objects.filter(order_id=order_id).first()
            
            if not shipment:
                raise ValueError('No se encontró envío para este pedido')
            
            observer_logs.append(f"✓ Pedido #{order_id} encontrado")
            observer_logs.append(f"Cliente: {order.customer_email}")
            observer_logs.append(f"Estado anterior: {shipment.status}")
            observer_logs.append("")
            
            # Actualizar estado
            old_status = shipment.status
            shipment.status = new_status.upper()
            shipment.save()
            
            observer_logs.append(f"✓ Estado actualizado: {old_status} → {new_status.upper()}")
            observer_logs.append("")
            observer_logs.append("Iniciando sistema de notificaciones...")
            observer_logs.append("")
            
            # Disparar notificaciones con Observer
            subject = OrderNotificationSubject()
            observers = create_default_observers()
            
            observer_logs.append(f"Registrando {len(observers)} observers:")
            for observer in observers:
                subject.attach(observer)
                observer_name = observer.__class__.__name__
                observer_logs.append(f"  ├─ {observer_name}")
            
            observer_logs.append("")
            observer_logs.append("Notificando a todos los observers...")
            
            notification_data = {
                'order_id': order.id,
                'order_code': f'PKG-{order.id:08X}',
                'customer_email': order.customer_email,
                'tracking_code': shipment.tracking_id,
                'provider_name': shipment.provider,
                'weight': order.total_weight,
                'priority': order.priority,
                'fragility': order.fragility,
                'status': new_status,
                'pickup_date': str(order.created_at)
            }
            
            subject.notify(notification_data)
            
            # Contar notificaciones
            new_notifications = Notification.objects.filter(
                order_id=order.id,
                message__contains=new_status
            ).count()
            
            observer_logs.append("")
            observer_logs.append(f"✓ Notificaciones completadas:")
            observer_logs.append(f"  └─ {new_notifications} notificaciones nuevas enviadas")
            observer_logs.append(f"  └─ Total notificaciones del pedido: {Notification.objects.filter(order_id=order.id).count()}")
            
            # Retornar lista de canales notificados
            return [obs.get_observer_name() for obs in observers]
            
        except Order.DoesNotExist:
            raise ValueError(f'Pedido #{order_id} no encontrado')


def get_order_processing_info(order_id: int) -> Dict[str, Any]:
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
