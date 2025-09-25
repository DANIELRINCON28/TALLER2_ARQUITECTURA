"""
Funciones de negocio para la aplicación de pedidos.
Refactorizado para implementar patrones de diseño:
- CREACIONAL: Builder (para construcción compleja de pedidos)
- ESTRUCTURAL: Adapter (para unificar APIs de proveedores)
- COMPORTAMENTAL: Strategy + Observer (para selección de proveedores y notificaciones)
"""
import secrets
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Protocol
from django.db import transaction
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Product, Order, OrderItem, Shipment, Notification


# ==========================================
# PATRÓN CREACIONAL: BUILDER
# ==========================================

class OrderBuilder:
    """
    Builder para la construcción compleja de pedidos.
    Encapsula la lógica de validación, cálculo de pesos, generación de códigos, etc.
    Reemplaza la lógica compleja en handle_create_order().
    """
    
    def __init__(self):
        self._reset()
    
    def _reset(self):
        """Reinicia el builder para construir un nuevo pedido."""
        self._customer_email = None
        self._address = None
        self._priority = 'normal'
        self._fragility = 'ninguna'
        self._items = {}
        self._resolved_items = []
        self._total_weight = 0
        self._package_code = None
        self._handling_label = None
        self._estimated_pickup_date = None
    
    def with_customer(self, email: str) -> 'OrderBuilder':
        """
        Establece el email del cliente con validación.
        
        Args:
            email: Email del cliente
            
        Returns:
            Self para method chaining
            
        Raises:
            ValueError: Si el email no es válido
        """
        email = email.strip()
        try:
            validate_email(email)
            self._customer_email = email
            return self
        except ValidationError:
            raise ValueError('Email inválido')
    
    def with_address(self, address: str) -> 'OrderBuilder':
        """
        Establece la dirección de entrega con validación.
        
        Args:
            address: Dirección de entrega
            
        Returns:
            Self para method chaining
            
        Raises:
            ValueError: Si la dirección está vacía
        """
        address = address.strip()
        if not address:
            raise ValueError('Dirección requerida')
        self._address = address
        return self
    
    def with_priority(self, priority: str) -> 'OrderBuilder':
        """
        Establece la prioridad del pedido.
        
        Args:
            priority: 'normal' o 'express'
            
        Returns:
            Self para method chaining
        """
        self._priority = priority if priority in ['normal', 'express'] else 'normal'
        return self
    
    def with_fragility(self, fragility: str) -> 'OrderBuilder':
        """
        Establece el nivel de fragilidad del pedido.
        
        Args:
            fragility: 'ninguna', 'debil' o 'alta'
            
        Returns:
            Self para method chaining
        """
        valid_options = ['ninguna', 'debil', 'alta']
        self._fragility = fragility if fragility in valid_options else 'ninguna'
        return self
    
    def with_items(self, items: Dict[str, int]) -> 'OrderBuilder':
        """
        Añade items al pedido y resuelve productos con cálculo de peso.
        
        Args:
            items: Diccionario {product_id: quantity}
            
        Returns:
            Self para method chaining
            
        Raises:
            ValueError: Si no hay items válidos
        """
        self._items = items
        self._resolve_items()
        return self
    
    def _resolve_items(self):
        """
        Resuelve los items del pedido validando productos y calculando peso total.
        Lógica extraída de handle_create_order().
        """
        self._total_weight = 0
        self._resolved_items = []
        
        for product_id, qty in self._items.items():
            qty = int(qty)
            if qty <= 0:
                continue
                
            try:
                product = Product.objects.get(id=product_id)
                self._total_weight += (product.weight_grams * qty)
                self._resolved_items.append({
                    'product_id': product.id,
                    'quantity': qty
                })
            except Product.DoesNotExist:
                continue
        
        if not self._resolved_items:
            raise ValueError('El pedido no tiene items válidos')
    
    def _generate_package_attributes(self):
        """
        Genera atributos adicionales del paquete según los requisitos:
        - codigoPaquete: código único generado
        - pesoEstimado: peso calculado 
        - etiquetaManejo: etiqueta según fragilidad
        - fechaRecogidaEstimada: fecha estimada de recogida
        """
        # Generar código único del paquete
        self._package_code = f"PKG-{secrets.token_hex(6).upper()}"
        
        # Generar etiqueta de manejo según fragilidad
        if self._fragility == 'alta':
            self._handling_label = "FRÁGIL - MANEJAR CON EXTREMO CUIDADO"
        elif self._fragility == 'debil':
            self._handling_label = "FRÁGIL"
        else:
            self._handling_label = "NORMAL"
        
        # Calcular fecha de recogida estimada (24-48 horas según prioridad)
        hours_offset = 24 if self._priority == 'express' else 48
        self._estimated_pickup_date = datetime.now() + timedelta(hours=hours_offset)
    
    def build(self) -> Order:
        """
        Construye y persiste el pedido con todos sus items.
        
        Returns:
            Instancia del pedido creado
            
        Raises:
            ValueError: Si faltan datos requeridos
        """
        # Validar datos requeridos
        if not self._customer_email:
            raise ValueError('Email del cliente requerido')
        if not self._address:
            raise ValueError('Dirección requerida')
        if not self._resolved_items:
            raise ValueError('Items del pedido requeridos')
        
        # Generar atributos del paquete
        self._generate_package_attributes()
        
        # Crear pedido en la base de datos
        with transaction.atomic():
            order = Order.objects.create(
                customer_email=self._customer_email,
                address=self._address,
                priority=self._priority,
                fragility=self._fragility,
                total_weight=self._total_weight
            )
            
            # Crear items del pedido
            for item in self._resolved_items:
                OrderItem.objects.create(
                    order_id=order.id,
                    product_id=item['product_id'],
                    quantity=item['quantity']
                )
            
            # Resetear builder para siguiente uso
            current_order = order
            self._reset()
            
            return current_order
    
    def get_order_summary(self) -> Dict[str, Any]:
        """
        Obtiene un resumen del pedido en construcción para debug/logging.
        
        Returns:
            Diccionario con resumen del pedido
        """
        if not hasattr(self, '_package_code') or not self._package_code:
            self._generate_package_attributes()
            
        return {
            'customer_email': self._customer_email,
            'address': self._address,
            'priority': self._priority,
            'fragility': self._fragility,
            'total_weight': self._total_weight,
            'items_count': len(self._resolved_items),
            'package_code': self._package_code,
            'handling_label': self._handling_label,
            'estimated_pickup_date': self._estimated_pickup_date.isoformat() if self._estimated_pickup_date else None
        }


# ==========================================
# PATRÓN ESTRUCTURAL: ADAPTER  
# ==========================================

class ShippingProvider(Protocol):
    """
    Interfaz común para todos los proveedores de envío.
    Define el contrato que deben cumplir todos los adapters.
    """
    
    def request_pickup(self, order_data: Dict[str, Any]) -> str:
        """
        Solicita recogida del pedido al proveedor.
        
        Args:
            order_data: Datos del pedido
            
        Returns:
            Código de tracking generado por el proveedor
        """
        ...
    
    def get_provider_name(self) -> str:
        """
        Obtiene el nombre del proveedor.
        
        Returns:
            Nombre del proveedor
        """
        ...


class MotoYAProvider:
    """
    Clase que simula la API específica de MotoYA.
    Representa un servicio externo con su propia interfaz.
    """
    
    def create_delivery_request(self, weight_kg: float, destination: str) -> Dict[str, str]:
        """
        Método específico de la API de MotoYA.
        Simula la creación de una solicitud de entrega.
        """
        tracking_code = f'MYA-{secrets.token_hex(3).upper()}'
        return {
            'delivery_id': tracking_code,
            'status': 'ACCEPTED',
            'estimated_time': '2-4 hours'
        }


class EcoBikeProvider:
    """
    Clase que simula la API específica de EcoBike.
    Representa un servicio externo con interfaz diferente a MotoYA.
    """
    
    def schedule_pickup(self, package_info: Dict[str, Any]) -> str:
        """
        Método específico de la API de EcoBike.
        Simula la programación de recogida ecológica.
        """
        return f'EBK-{secrets.token_hex(3).upper()}'


class PaqueteriaZProvider:
    """
    Clase que simula la API específica de PaqueteríaZ.
    Representa un servicio externo con otra interfaz diferente.
    """
    
    def submit_shipment(self, sender: str, recipient: str, weight: int) -> Dict[str, Any]:
        """
        Método específico de la API de PaqueteríaZ.
        Simula el envío de un paquete tradicional.
        """
        tracking_number = f'PAQ-{secrets.token_hex(3).upper()}'
        return {
            'tracking_number': tracking_number,
            'service_type': 'STANDARD',
            'delivery_days': '3-5'
        }


class MotoYAAdapter:
    """
    Adapter para MotoYA que implementa la interfaz común ShippingProvider.
    Traduce las llamadas de la interfaz común a la API específica de MotoYA.
    """
    
    def __init__(self):
        self._provider = MotoYAProvider()
    
    def request_pickup(self, order_data: Dict[str, Any]) -> str:
        """
        Adapta la solicitud común a la API específica de MotoYA.
        
        Args:
            order_data: Datos estándar del pedido
            
        Returns:
            Código de tracking de MotoYA
        """
        weight_kg = order_data.get('weight', 0) / 1000  # Convertir gramos a kg
        destination = order_data.get('address', '')
        
        response = self._provider.create_delivery_request(weight_kg, destination)
        return response['delivery_id']
    
    def get_provider_name(self) -> str:
        return 'motoya'


class EcoBikeAdapter:
    """
    Adapter para EcoBike que implementa la interfaz común ShippingProvider.
    Traduce las llamadas de la interfaz común a la API específica de EcoBike.
    """
    
    def __init__(self):
        self._provider = EcoBikeProvider()
    
    def request_pickup(self, order_data: Dict[str, Any]) -> str:
        """
        Adapta la solicitud común a la API específica de EcoBike.
        
        Args:
            order_data: Datos estándar del pedido
            
        Returns:
            Código de tracking de EcoBike
        """
        package_info = {
            'weight_grams': order_data.get('weight', 0),
            'fragile': order_data.get('fragility', 'ninguna') != 'ninguna',
            'priority': order_data.get('priority', 'normal'),
            'destination': order_data.get('address', '')
        }
        
        return self._provider.schedule_pickup(package_info)
    
    def get_provider_name(self) -> str:
        return 'ecobike'


class PaqueteriaZAdapter:
    """
    Adapter para PaqueteríaZ que implementa la interfaz común ShippingProvider.
    Traduce las llamadas de la interfaz común a la API específica de PaqueteríaZ.
    """
    
    def __init__(self):
        self._provider = PaqueteriaZProvider()
    
    def request_pickup(self, order_data: Dict[str, Any]) -> str:
        """
        Adapta la solicitud común a la API específica de PaqueteríaZ.
        
        Args:
            order_data: Datos estándar del pedido
            
        Returns:
            Código de tracking de PaqueteríaZ
        """
        sender = "MercadoBarrio Warehouse"
        recipient = order_data.get('address', '')
        weight = order_data.get('weight', 0)
        
        response = self._provider.submit_shipment(sender, recipient, weight)
        return response['tracking_number']
    
    def get_provider_name(self) -> str:
        return 'paqz'


class ShippingAdapterFactory:
    """
    Factory para crear adapters de proveedores de envío.
    Encapsula la creación de adapters y permite fácil extensión.
    """
    
    _adapters = {
        'motoya': MotoYAAdapter,
        'ecobike': EcoBikeAdapter,
        'paqz': PaqueteriaZAdapter
    }
    
    @classmethod
    def create_adapter(cls, provider_name: str) -> ShippingProvider:
        """
        Crea un adapter para el proveedor especificado.
        
        Args:
            provider_name: Nombre del proveedor ('motoya', 'ecobike', 'paqz')
            
        Returns:
            Instancia del adapter correspondiente
            
        Raises:
            ValueError: Si el proveedor no es válido
        """
        adapter_class = cls._adapters.get(provider_name.lower())
        if not adapter_class:
            available = ', '.join(cls._adapters.keys())
            raise ValueError(f'Proveedor no válido: {provider_name}. Disponibles: {available}')
        
        return adapter_class()
    
    @classmethod
    def get_available_providers(cls) -> List[str]:
        """
        Obtiene la lista de proveedores disponibles.
        
        Returns:
            Lista de nombres de proveedores
        """
        return list(cls._adapters.keys())


# ==========================================
# PATRÓN COMPORTAMENTAL: STRATEGY
# ==========================================

class ProviderSelectionStrategy(ABC):
    """
    Estrategia abstracta para la selección de proveedores de envío.
    Define la interfaz común para diferentes algoritmos de selección.
    """
    
    @abstractmethod
    def select_provider(self, order_data: Dict[str, Any]) -> str:
        """
        Selecciona un proveedor basado en los datos del pedido.
        
        Args:
            order_data: Datos del pedido para tomar la decisión
            
        Returns:
            Nombre del proveedor seleccionado
        """
        pass
    
    @abstractmethod
    def get_strategy_name(self) -> str:
        """
        Obtiene el nombre de la estrategia.
        
        Returns:
            Nombre descriptivo de la estrategia
        """
        pass


class StandardSelectionStrategy(ProviderSelectionStrategy):
    """
    Estrategia estándar de selección de proveedores.
    Implementa la lógica original de select_provider_naive().
    Prioriza velocidad y costo según las reglas de negocio básicas.
    """
    
    def select_provider(self, order_data: Dict[str, Any]) -> str:
        """
        Selecciona proveedor usando la lógica estándar:
        1. Express + frágil → EcoBike
        2. Peso ligero (≤1200g) → MotoYA  
        3. Resto → PaqueteríaZ
        """
        priority = order_data.get('priority', 'normal')
        fragility = order_data.get('fragility', 'ninguna')
        total_weight = order_data.get('weight', 0)
        
        # Regla 1: Express y frágil prefiere EcoBike
        if priority == 'express' and fragility != 'ninguna':
            return 'ecobike'
        
        # Regla 2: Peso ligero prefiere MotoYA (rápido en ciudad)
        if total_weight <= 1200:
            return 'motoya'
        
        # Regla 3: Resto usa PaqueteríaZ (para pesos altos y distancias largas)
        return 'paqz'
    
    def get_strategy_name(self) -> str:
        return 'Selección Estándar (velocidad/costo)'


class EcoFriendlySelectionStrategy(ProviderSelectionStrategy):
    """
    Estrategia de selección ecológica.
    Prioriza proveedores con menor impacto ambiental.
    """
    
    def select_provider(self, order_data: Dict[str, Any]) -> str:
        """
        Selecciona proveedor priorizando impacto ambiental:
        1. Siempre prefiere EcoBike si el peso lo permite
        2. MotoYA para casos donde EcoBike no es viable
        3. PaqueteríaZ solo cuando no hay alternativa
        """
        total_weight = order_data.get('weight', 0)
        fragility = order_data.get('fragility', 'ninguna')
        
        # EcoBike tiene límite de peso (ej: 2kg) pero es ecológico
        if total_weight <= 2000:
            return 'ecobike'
        
        # MotoYA es menos ecológico pero más rápido que PaqueteríaZ
        if total_weight <= 5000 and fragility != 'alta':
            return 'motoya'
        
        # PaqueteríaZ para casos pesados o muy frágiles
        return 'paqz'
    
    def get_strategy_name(self) -> str:
        return 'Selección Ecológica (menor impacto ambiental)'


class CostOptimizedSelectionStrategy(ProviderSelectionStrategy):
    """
    Estrategia de selección optimizada por costo.
    Prioriza el proveedor más económico según el tipo de pedido.
    """
    
    def select_provider(self, order_data: Dict[str, Any]) -> str:
        """
        Selecciona proveedor optimizando costos:
        1. PaqueteríaZ para pesos altos (más eficiente)
        2. MotoYA para entregas urbanas normales
        3. EcoBike solo para express frágiles (valor agregado)
        """
        priority = order_data.get('priority', 'normal')
        fragility = order_data.get('fragility', 'ninguna')
        total_weight = order_data.get('weight', 0)
        
        # PaqueteríaZ es más barato para pesos altos
        if total_weight > 3000:
            return 'paqz'
        
        # EcoBike solo si es express y frágil (justifica el costo premium)
        if priority == 'express' and fragility == 'alta':
            return 'ecobike'
        
        # MotoYA para el resto (buen balance costo/velocidad)
        return 'motoya'
    
    def get_strategy_name(self) -> str:
        return 'Selección Optimizada por Costo'


class ProviderSelector:
    """
    Contexto que utiliza diferentes estrategias de selección de proveedores.
    Permite cambiar algoritmos de selección dinámicamente.
    """
    
    def __init__(self, strategy: ProviderSelectionStrategy = None):
        """
        Inicializa el selector con una estrategia.
        
        Args:
            strategy: Estrategia de selección a usar (por defecto: estándar)
        """
        self._strategy = strategy or StandardSelectionStrategy()
    
    def set_strategy(self, strategy: ProviderSelectionStrategy):
        """
        Cambia la estrategia de selección.
        
        Args:
            strategy: Nueva estrategia a usar
        """
        self._strategy = strategy
    
    def select_provider(self, order_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Selecciona un proveedor usando la estrategia actual.
        
        Args:
            order_data: Datos del pedido
            
        Returns:
            Diccionario con el proveedor seleccionado y la estrategia usada
        """
        selected_provider = self._strategy.select_provider(order_data)
        
        return {
            'provider': selected_provider,
            'strategy': self._strategy.get_strategy_name(),
            'reason': self._get_selection_reason(order_data, selected_provider)
        }
    
    def _get_selection_reason(self, order_data: Dict[str, Any], provider: str) -> str:
        """
        Genera una explicación de por qué se seleccionó el proveedor.
        
        Args:
            order_data: Datos del pedido
            provider: Proveedor seleccionado
            
        Returns:
            Explicación textual de la selección
        """
        weight = order_data.get('weight', 0)
        priority = order_data.get('priority', 'normal')
        fragility = order_data.get('fragility', 'ninguna')
        
        return f"Proveedor {provider} seleccionado para pedido de {weight}g, prioridad {priority}, fragilidad {fragility}"


# ==========================================
# PATRÓN COMPORTAMENTAL: OBSERVER
# ==========================================

def truncate_message_for_db(message: str, max_length: int = 255) -> str:
    """
    Trunca un mensaje para que pueda ser almacenado en la base de datos.
    
    Args:
        message: Mensaje original
        max_length: Longitud máxima permitida (por defecto 255 caracteres)
        
    Returns:
        Mensaje truncado si es necesario
    """
    if len(message) <= max_length:
        return message
    
    # Truncar dejando espacio para "..."
    truncated = message[:max_length - 3] + "..."
    return truncated

class OrderObserver(ABC):
    """
    Interfaz abstracta para observadores de cambios en pedidos.
    Define el contrato para recibir notificaciones de eventos.
    """
    
    @abstractmethod
    def notify(self, order: Order, event_type: str, message: str) -> None:
        """
        Recibe notificación de un evento en el pedido.
        
        Args:
            order: Instancia del pedido
            event_type: Tipo de evento ('CREATED', 'DISPATCHED', 'IN_TRANSIT', 'DELIVERED')
            message: Mensaje descriptivo del evento
        """
        pass
    
    @abstractmethod
    def get_observer_name(self) -> str:
        """
        Obtiene el nombre del observador.
        
        Returns:
            Nombre descriptivo del observador
        """
        pass


class EmailNotificationObserver(OrderObserver):
    """
    Observador que envía notificaciones por email.
    Simula el envío de emails al cliente cuando cambia el estado del pedido.
    """
    
    def notify(self, order: Order, event_type: str, message: str) -> None:
        """
        Envía notificación por email (simulado).
        En implementación real aquí iría la lógica de envío de email.
        """
        # Simular envío de email
        email_content = self._generate_email_content(order, event_type, message)
        
        # Truncar mensaje para BD si es necesario
        db_message = truncate_message_for_db(email_content)
        
        # Persistir notificación en base de datos
        Notification.objects.create(
            order=order,
            channel='email',
            message=db_message
        )
        
        # Log para demostración
        print(f"📧 EMAIL enviado a {order.customer_email}: {email_content}")
    
    def _generate_email_content(self, order: Order, event_type: str, message: str) -> str:
        """
        Genera el contenido del email según el tipo de evento.
        """
        templates = {
            'CREATED': f"¡Pedido #{order.id} confirmado! {message}",
            'DISPATCHED': f"📦 Pedido #{order.id} despachado. {message}",
            'IN_TRANSIT': f"🚚 Pedido #{order.id} en camino. {message}",
            'DELIVERED': f"✅ Pedido #{order.id} entregado. {message}"
        }
        
        return templates.get(event_type, f"Pedido #{order.id}: {message}")
    
    def get_observer_name(self) -> str:
        return 'Notificador Email'


class WebhookNotificationObserver(OrderObserver):
    """
    Observador que envía notificaciones via webhook.
    Simula llamadas HTTP a sistemas externos cuando cambia el estado del pedido.
    """
    
    def __init__(self, webhook_url: str = None):
        """
        Inicializa el observador webhook.
        
        Args:
            webhook_url: URL del webhook (opcional, para simulación)
        """
        self._webhook_url = webhook_url or "https://api.external-system.com/webhook"
    
    def notify(self, order: Order, event_type: str, message: str) -> None:
        """
        Envía notificación via webhook (simulado).
        En implementación real aquí iría la llamada HTTP real.
        """
        webhook_payload = self._generate_webhook_payload(order, event_type, message)
        
        # Crear mensaje resumido para BD
        db_message = f"Webhook a {self._webhook_url}: {event_type} para pedido #{order.id}"
        db_message = truncate_message_for_db(db_message)
        
        # Persistir notificación en base de datos
        Notification.objects.create(
            order=order,
            channel='webhook',
            message=db_message
        )
        
        # Log para demostración (en real sería una llamada HTTP)
        print(f"🔗 WEBHOOK enviado a {self._webhook_url}: {webhook_payload}")
    
    def _generate_webhook_payload(self, order: Order, event_type: str, message: str) -> str:
        """
        Genera el payload JSON para el webhook.
        """
        import json
        
        payload = {
            'order_id': order.id,
            'customer_email': order.customer_email,
            'event_type': event_type,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'priority': order.priority,
            'total_weight': order.total_weight
        }
        
        return json.dumps(payload)
    
    def get_observer_name(self) -> str:
        return f'Notificador Webhook ({self._webhook_url})'


class SMSNotificationObserver(OrderObserver):
    """
    Observador que envía notificaciones por SMS.
    Ejemplo de extensibilidad: fácil agregar nuevos canales.
    """
    
    def __init__(self, phone_number: str = None):
        self._phone_number = phone_number or "+1234567890"
    
    def notify(self, order: Order, event_type: str, message: str) -> None:
        """
        Envía notificación por SMS (simulado).
        """
        sms_content = self._generate_sms_content(order, event_type, message)
        
        # Truncar mensaje para BD si es necesario (SMS ya es corto, pero por precaución)
        db_message = truncate_message_for_db(sms_content)
        
        # Persistir notificación en base de datos
        Notification.objects.create(
            order=order,
            channel='sms',
            message=db_message
        )
        
        # Log para demostración
        print(f"📱 SMS enviado a {self._phone_number}: {sms_content}")
    
    def _generate_sms_content(self, order: Order, event_type: str, message: str) -> str:
        """
        Genera contenido corto para SMS.
        """
        short_messages = {
            'CREATED': f"Pedido #{order.id} confirmado",
            'DISPATCHED': f"Pedido #{order.id} despachado",
            'IN_TRANSIT': f"Pedido #{order.id} en camino",
            'DELIVERED': f"Pedido #{order.id} entregado"
        }
        
        return short_messages.get(event_type, f"Pedido #{order.id} actualizado")
    
    def get_observer_name(self) -> str:
        return f'Notificador SMS ({self._phone_number})'


class OrderNotificationSubject:
    """
    Sujeto observable que gestiona los observadores de pedidos.
    Mantiene la lista de observadores y los notifica cuando ocurren eventos.
    """
    
    def __init__(self):
        """
        Inicializa el sujeto con lista vacía de observadores.
        """
        self._observers: List[OrderObserver] = []
        self._notification_history: List[Dict[str, Any]] = []
    
    def attach_observer(self, observer: OrderObserver) -> None:
        """
        Agrega un observador a la lista.
        
        Args:
            observer: Observador a agregar
        """
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"➕ Observador agregado: {observer.get_observer_name()}")
    
    def detach_observer(self, observer: OrderObserver) -> None:
        """
        Remueve un observador de la lista.
        
        Args:
            observer: Observador a remover
        """
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"➖ Observador removido: {observer.get_observer_name()}")
    
    def notify_observers(self, order: Order, event_type: str, message: str) -> None:
        """
        Notifica a todos los observadores sobre un evento.
        
        Args:
            order: Pedido relacionado con el evento
            event_type: Tipo de evento
            message: Mensaje del evento
        """
        print(f"\n🔔 Notificando evento {event_type} para pedido #{order.id}")
        print(f"   Observadores activos: {len(self._observers)}")
        
        # Registrar en historial
        event_record = {
            'order_id': order.id,
            'event_type': event_type,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'observers_count': len(self._observers)
        }
        self._notification_history.append(event_record)
        
        # Notificar a todos los observadores
        for observer in self._observers:
            try:
                observer.notify(order, event_type, message)
            except Exception as e:
                print(f"❌ Error en observador {observer.get_observer_name()}: {e}")
    
    def get_observers_info(self) -> List[str]:
        """
        Obtiene información de los observadores activos.
        
        Returns:
            Lista con nombres de observadores activos
        """
        return [observer.get_observer_name() for observer in self._observers]
    
    def get_notification_history(self) -> List[Dict[str, Any]]:
        """
        Obtiene el historial de notificaciones.
        
        Returns:
            Lista con historial de eventos notificados
        """
        return self._notification_history.copy()


# ==========================================
# FUNCIONES PÚBLICAS REFACTORIZADAS
# ==========================================

def products_all() -> List[Product]:
    """
    Obtiene todos los productos ordenados por nombre.
    Función utilitaria sin cambios (no requiere patrones).
    """
    return list(Product.objects.all().order_by('name'))


def orders_latest(limit: int = 5) -> List[Order]:
    """
    Obtiene los últimos pedidos limitados por cantidad.
    Función utilitaria sin cambios (no requiere patrones).
    """
    return list(Order.objects.all().order_by('-id')[:limit])


def order_with_items(order_id: int) -> Optional[Dict[str, Any]]:
    """
    Obtiene un pedido con sus items asociados.
    Función utilitaria sin cambios (no requiere patrones).
    """
    try:
        order = Order.objects.get(id=order_id)
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
    Función utilitaria sin cambios (no requiere patrones).
    """
    try:
        return Shipment.objects.filter(order_id=order_id).order_by('-id').first()
    except Shipment.DoesNotExist:
        return None


def handle_create_order(input_data: Dict[str, Any], strategy_type: str = 'standard') -> int:
    """
    FUNCIÓN PRINCIPAL REFACTORIZADA CON PATRONES DE DISEÑO
    
    Maneja la creación completa de un pedido utilizando:
    - BUILDER: Para construcción compleja del pedido
    - ADAPTER: Para integración uniforme con proveedores
    - STRATEGY: Para selección inteligente de proveedores  
    - OBSERVER: Para notificaciones multi-canal
    
    Args:
        input_data: Diccionario con datos del formulario
        strategy_type: Tipo de estrategia ('standard', 'eco', 'cost')
        
    Returns:
        ID del pedido creado
        
    Raises:
        ValueError: Si los datos de entrada no son válidos
    """
    print("🚀 Iniciando creación de pedido con patrones de diseño")
    print("=" * 60)
    
    try:
        # ============================================
        # PATRÓN BUILDER: Construcción del pedido
        # ============================================
        print("🔨 Aplicando patrón BUILDER para construcción del pedido...")
        
        builder = OrderBuilder()
        order = (builder
                .with_customer(input_data.get('customer_email', ''))
                .with_address(input_data.get('address', ''))
                .with_priority(input_data.get('priority', 'normal'))
                .with_fragility(input_data.get('fragility', 'ninguna'))
                .with_items(input_data.get('items', {}))
                .build())
        
        # Obtener resumen del pedido construido
        order_summary = builder.get_order_summary()
        print(f"   ✅ Pedido #{order.id} construido exitosamente")
        print(f"   📦 Código paquete: {order_summary['package_code']}")
        print(f"   🏷️  Etiqueta manejo: {order_summary['handling_label']}")
        print(f"   ⚖️  Peso total: {order_summary['total_weight']}g")
        print(f"   📅 Recogida estimada: {order_summary['estimated_pickup_date']}")
        
        # ============================================
        # PATRÓN STRATEGY: Selección de proveedor
        # ============================================
        print(f"\n📋 Aplicando patrón STRATEGY ({strategy_type}) para selección de proveedor...")
        
        # Configurar estrategia según parámetro
        strategies = {
            'standard': StandardSelectionStrategy(),
            'eco': EcoFriendlySelectionStrategy(),
            'cost': CostOptimizedSelectionStrategy()
        }
        
        strategy = strategies.get(strategy_type, StandardSelectionStrategy())
        selector = ProviderSelector(strategy)
        
        # Datos para selección de proveedor
        selection_data = {
            'priority': order.priority,
            'fragility': order.fragility,
            'weight': order.total_weight,
            'address': order.address
        }
        
        selection_result = selector.select_provider(selection_data)
        selected_provider = selection_result['provider']
        
        print(f"   ✅ Proveedor seleccionado: {selected_provider}")
        print(f"   📊 Estrategia usada: {selection_result['strategy']}")
        print(f"   💡 Razón: {selection_result['reason']}")
        
        # ============================================
        # PATRÓN ADAPTER: Integración con proveedor
        # ============================================
        print(f"\n🔌 Aplicando patrón ADAPTER para integración con {selected_provider}...")
        
        try:
            # Crear adapter apropiado usando factory
            provider_adapter = ShippingAdapterFactory.create_adapter(selected_provider)
            
            # Datos estandarizados para el adapter
            adapter_data = {
                'order_id': order.id,
                'weight': order.total_weight,
                'priority': order.priority,
                'fragility': order.fragility,
                'address': order.address
            }
            
            # Solicitar recogida usando interfaz unificada
            tracking_id = provider_adapter.request_pickup(adapter_data)
            
            print(f"   ✅ Integración exitosa con {provider_adapter.get_provider_name()}")
            print(f"   🏷️  Tracking ID: {tracking_id}")
            
        except ValueError as e:
            print(f"   ❌ Error en adapter: {e}")
            raise
        
        # Registrar envío en base de datos
        with transaction.atomic():
            shipment = Shipment.objects.create(
                order=order,
                provider=selected_provider,
                tracking_id=tracking_id,
                status='CONFIRMADO'
            )
            
            print(f"   💾 Envío registrado en BD: {shipment}")
        
        # ============================================
        # PATRÓN OBSERVER: Sistema de notificaciones
        # ============================================
        print(f"\n🔔 Aplicando patrón OBSERVER para notificaciones...")
        
        # Configurar sujeto observable
        notification_subject = OrderNotificationSubject()
        
        # Configurar observadores (canales de notificación)
        email_observer = EmailNotificationObserver()
        webhook_observer = WebhookNotificationObserver()
        sms_observer = SMSNotificationObserver()
        
        # Registrar observadores
        notification_subject.attach_observer(email_observer)
        notification_subject.attach_observer(webhook_observer)
        notification_subject.attach_observer(sms_observer)
        
        # Notificar evento de creación de pedido
        confirmation_message = (
            f"Pedido confirmado y asignado a {selected_provider} "
            f"con tracking {tracking_id}. "
            f"Estrategia usada: {selection_result['strategy']}"
        )
        
        notification_subject.notify_observers(order, 'CREATED', confirmation_message)
        
        print(f"   ✅ Notificaciones enviadas a {len(notification_subject.get_observers_info())} canales")
        print(f"   📝 Canales activos: {', '.join(notification_subject.get_observers_info())}")
        
        # ============================================
        # RESUMEN FINAL
        # ============================================
        print("\n" + "=" * 60)
        print("🎉 PEDIDO CREADO EXITOSAMENTE CON PATRONES DE DISEÑO")
        print("=" * 60)
        print(f"📋 Pedido ID: #{order.id}")
        print(f"👤 Cliente: {order.customer_email}")
        print(f"📍 Dirección: {order.address}")
        print(f"🚚 Proveedor: {selected_provider} (tracking: {tracking_id})")
        print(f"📊 Estrategia: {selection_result['strategy']}")
        print(f"🔔 Notificaciones: {len(notification_subject.get_observers_info())} canales")
        print("=" * 60)
        
        return order.id
        
    except Exception as e:
        print(f"\n❌ ERROR en creación de pedido: {e}")
        raise


# ==========================================
# FUNCIONES LEGACY (COMPATIBILIDAD)
# ==========================================

def select_provider_naive(priority: str, fragility: str, total_weight: int) -> str:
    """
    FUNCIÓN LEGACY: Mantenida para compatibilidad.
    USO RECOMENDADO: Usar ProviderSelector con Strategy pattern.
    
    Selecciona proveedor usando lógica simple con if/else.
    """
    print("⚠️  ADVERTENCIA: Usando función legacy select_provider_naive")
    print("   💡 Recomendación: Migrar a ProviderSelector con patrón Strategy")
    
    if priority == 'express' and fragility != 'ninguna':
        return 'ecobike'
    if total_weight <= 1200:
        return 'motoya'
    return 'paqz'


def request_pickup_naive(provider: str, data: Dict[str, Any]) -> str:
    """
    FUNCIÓN LEGACY: Mantenida para compatibilidad.
    USO RECOMENDADO: Usar ShippingAdapterFactory con Adapter pattern.
    
    Simula distintas formas de generar tracking por proveedor.
    """
    print("⚠️  ADVERTENCIA: Usando función legacy request_pickup_naive")
    print("   💡 Recomendación: Migrar a ShippingAdapterFactory con patrón Adapter")
    
    if provider == 'motoya':
        return f'MYA-{secrets.token_hex(3).upper()}'
    elif provider == 'ecobibe':
        return f'EBK-{secrets.token_hex(3).upper()}'
    else:
        return f'PAQ-{secrets.token_hex(3).upper()}'


# ==========================================
# SERVICIO PRINCIPAL CON PATRONES INTEGRADOS
# ==========================================

class OrderService:
    """
    Servicio principal que integra todos los patrones de diseño.
    Proporciona una interfaz de alto nivel para la creación y gestión de pedidos.
    """
    
    def __init__(self):
        """Inicializa el servicio con configuración por defecto."""
        self.notification_subject = OrderNotificationSubject()
        
    def create_order_with_patterns(
        self,
        customer_email: str,
        address: str,
        priority: str,
        fragility: str,
        items: Dict[str, int],
        strategy: str = 'standard'
    ) -> Dict[str, Any]:
        """
        Crea un pedido utilizando todos los patrones de diseño implementados.
        
        Args:
            customer_email: Email del cliente
            address: Dirección de entrega
            priority: Prioridad del pedido ('normal' | 'express')
            fragility: Nivel de fragilidad ('ninguna' | 'debil' | 'alta')
            items: Items del pedido {product_id: quantity}
            strategy: Estrategia de selección ('standard' | 'eco' | 'cost')
            
        Returns:
            Diccionario con información del pedido creado y patrones utilizados
        """
        # Configurar observadores
        self._setup_observers()
        
        # Crear pedido usando handle_create_order con patrones
        input_data = {
            'customer_email': customer_email,
            'address': address,
            'priority': priority,
            'fragility': fragility,
            'items': items
        }
        
        order_id = handle_create_order(input_data, strategy)
        
        # Obtener información detallada del pedido creado
        order_info = self._get_order_details(order_id)
        
        return {
            'order_id': order_id,
            'patterns_used': {
                'builder': 'Construcción compleja del pedido con validaciones',
                'strategy': order_info.get('strategy_used', 'Selección de proveedor'),
                'adapter': f"Integración con {order_info.get('provider', 'proveedor')}",
                'observer': f"Notificaciones a {len(self.notification_subject.get_observers_info())} canales"
            },
            'order_details': order_info
        }
    
    def _setup_observers(self):
        """Configura los observadores por defecto."""
        # Limpiar observadores existentes
        self.notification_subject = OrderNotificationSubject()
        
        # Agregar observadores estándar
        email_observer = EmailNotificationObserver()
        webhook_observer = WebhookNotificationObserver("https://api.external-system.com/webhook")
        sms_observer = SMSNotificationObserver("+1234567890")
        
        self.notification_subject.attach_observer(email_observer)
        self.notification_subject.attach_observer(webhook_observer)
        self.notification_subject.attach_observer(sms_observer)
    
    def _get_order_details(self, order_id: int) -> Dict[str, Any]:
        """Obtiene detalles completos del pedido."""
        try:
            order = Order.objects.get(id=order_id)
            shipment = Shipment.objects.filter(order_id=order_id).first()
            
            return {
                'order': order,
                'shipment': shipment,
                'provider': shipment.provider if shipment else None,
                'tracking_id': shipment.tracking_id if shipment else None,
                'strategy_used': 'Estrategia aplicada durante creación'
            }
        except Order.DoesNotExist:
            return {}
    
    def simulate_status_change(self, order_id: int, new_status: str) -> List[str]:
        """
        Simula cambio de estado del pedido para demostrar patrón Observer.
        
        Args:
            order_id: ID del pedido
            new_status: Nuevo estado del pedido
            
        Returns:
            Lista de canales notificados
        """
        try:
            order = Order.objects.get(id=order_id)
            
            # Configurar observadores si no están configurados
            if not self.notification_subject.get_observers_info():
                self._setup_observers()
            
            # Generar mensaje según el estado
            status_messages = {
                'dispatched': 'Pedido empacado y listo para recogida',
                'in_transit': 'Pedido en camino al destino',
                'delivered': 'Pedido entregado exitosamente'
            }
            
            message = status_messages.get(new_status, f'Estado cambiado a {new_status}')
            event_type = new_status.upper()
            
            # Notificar observadores
            self.notification_subject.notify_observers(order, event_type, message)
            
            return self.notification_subject.get_observers_info()
            
        except Order.DoesNotExist:
            raise ValueError(f'Pedido #{order_id} no encontrado')
    
    def get_order_status(self, order_id: int) -> Dict[str, Any]:
        """
        Obtiene el estado actual del pedido.
        
        Args:
            order_id: ID del pedido
            
        Returns:
            Información del estado del pedido
        """
        try:
            order = Order.objects.get(id=order_id)
            shipment = Shipment.objects.filter(order_id=order_id).first()
            notifications = Notification.objects.filter(order_id=order_id).count()
            
            return {
                'order_id': order_id,
                'customer_email': order.customer_email,
                'priority': order.priority,
                'status': shipment.status if shipment else 'PENDING',
                'provider': shipment.provider if shipment else None,
                'tracking_id': shipment.tracking_id if shipment else None,
                'notifications_sent': notifications
            }
            
        except Order.DoesNotExist:
            raise ValueError(f'Pedido #{order_id} no encontrado')


def get_order_processing_info(order_id: int) -> Dict[str, Any]:
    """
    Obtiene información detallada del procesamiento del pedido con patrones.
    
    Args:
        order_id: ID del pedido
        
    Returns:
        Información de patrones utilizados en el pedido
    """
    try:
        order = Order.objects.get(id=order_id)
        shipment = Shipment.objects.filter(order_id=order_id).first()
        notifications = list(Notification.objects.filter(order_id=order_id))
        
        # Simular información de patrones (en implementación real se obtendría de logs/metadata)
        return {
            'builder_info': {
                'pattern': 'Builder (Creacional)',
                'description': 'Construcción compleja del pedido con validaciones',
                'package_code': f'PKG-{order.id:08X}',  # Simular código generado
                'weight_calculated': order.total_weight,
                'fragility_handled': order.fragility != 'ninguna'
            },
            'strategy_info': {
                'pattern': 'Strategy (Comportamental)',
                'description': 'Selección inteligente de proveedor',
                'provider_selected': shipment.provider if shipment else 'N/A',
                'decision_factors': f'Peso: {order.total_weight}g, Prioridad: {order.priority}, Fragilidad: {order.fragility}'
            },
            'adapter_info': {
                'pattern': 'Adapter (Estructural)',
                'description': 'Integración unificada con APIs de proveedores',
                'provider_integrated': shipment.provider if shipment else 'N/A',
                'tracking_generated': shipment.tracking_id if shipment else 'N/A',
                'unified_interface': True
            },
            'observer_info': {
                'pattern': 'Observer (Comportamental)',
                'description': 'Sistema de notificaciones multi-canal',
                'notifications_sent': len(notifications),
                'channels_used': list(set([n.channel for n in notifications])),
                'auto_notification': True
            }
        }
        
    except Order.DoesNotExist:
        return {
            'error': f'Pedido #{order_id} no encontrado',
            'patterns_info': None
        }