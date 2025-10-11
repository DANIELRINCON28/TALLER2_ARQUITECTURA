from abc import ABC, abstractmethod
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


# ==========================================
# INTERFAZ OBSERVER
# ==========================================

class OrderObserver(ABC):
    """
    Interfaz abstracta para observadores de pedidos.
    Define el contrato que todos los observadores concretos deben cumplir.
    """
    
    @abstractmethod
    def update(self, order_data: Dict[str, Any]) -> None:
        pass
    
    def get_observer_name(self) -> str:
        return self.__class__.__name__


# ==========================================
# OBSERVADORES CONCRETOS
# ==========================================

class EmailNotificationObserver(OrderObserver):
    
    def update(self, order_data: Dict[str, Any]) -> None:
        """
        Envía notificación por email cuando se crea un pedido.
        """
        customer_email = order_data.get('customer_email')
        order_code = order_data.get('order_code')
        tracking_code = order_data.get('tracking_code')
        provider_name = order_data.get('provider_name', 'N/A')
        
        # Simular envío de email
        email_content = f"Pedido {order_code} confirmado. Tracking: {tracking_code}"
        
        logger.info(f"📧 Email enviado a {customer_email}")
        logger.info(f"Asunto: Pedido {order_code} confirmado")
        logger.info(f"Tracking: {tracking_code} ({provider_name})")
        logger.debug(f"Contenido: {email_content}")

class WebhookNotificationObserver(OrderObserver):
    
    def __init__(self, webhook_url: str = "https://example.com/webhook"):
        self.webhook_url = webhook_url
    
    def update(self, order_data: Dict[str, Any]) -> None:

        payload = self._prepare_webhook_payload(order_data)
        
        logger.info(f"🔗 Webhook disparado a {self.webhook_url}")
        logger.debug(f"Payload: {payload}")
        
        # En producción:
        # import requests
        # try:
        #     response = requests.post(
        #         self.webhook_url,
        #         json=payload,
        #         headers={'Content-Type': 'application/json'},
        #         timeout=10
        #     )
        #     response.raise_for_status()
        #     logger.info(f"Webhook exitoso: {response.status_code}")
        # except requests.RequestException as e:
        #     logger.error(f"Error en webhook: {e}")
    
    def _prepare_webhook_payload(self, order_data: Dict[str, Any]) -> Dict[str, Any]:

        return {
            'event': 'order.created',
            'timestamp': order_data.get('pickup_date'),
            'data': {
                'order_id': order_data.get('order_code'),
                'customer': order_data.get('customer_email'),
                'tracking': order_data.get('tracking_code'),
                'provider': order_data.get('provider_name'),
                'total_weight': order_data.get('weight'),
                'priority': order_data.get('priority'),
                'fragility': order_data.get('fragility')
            }
        }


class SMSNotificationObserver(OrderObserver):
    
    def update(self, order_data: Dict[str, Any]) -> None:
        """
        Envía notificación SMS cuando se crea un pedido de alta prioridad.
        """
        priority = order_data.get('priority', 'normal')
        
        # Solo enviar SMS para pedidos urgentes
        if priority != 'urgente':
            logger.debug(f"SMS omitido para pedido no urgente")
            return
        
        phone_number = self._extract_phone_number(order_data)
        message = self._generate_sms_message(order_data)
        
        logger.info(f"📱 SMS enviado a {phone_number}")
        logger.info(f"Mensaje: {message}")
 
    def _extract_phone_number(self, order_data: Dict[str, Any]) -> str:
        return "+52 1234567890"  # Simulado
    
    def _generate_sms_message(self, order_data: Dict[str, Any]) -> str:

        order_code = order_data.get('order_code', 'N/A')
        tracking_code = order_data.get('tracking_code', 'N/A')
        
        message = f"Pedido {order_code} confirmado. Tracking: {tracking_code}"
        
        return truncate_message_for_db(message, 160)


class LoggingObserver(OrderObserver):
    
    def update(self, order_data: Dict[str, Any]) -> None:
        """
        Registra la creación del pedido en los logs del sistema.
        """
        logger.info("=" * 60)
        logger.info("NUEVO PEDIDO CREADO")
        logger.info("=" * 60)
        logger.info(f"Código: {order_data.get('order_code')}")
        logger.info(f"Cliente: {order_data.get('customer_email')}")
        logger.info(f"Tracking: {order_data.get('tracking_code')}")
        logger.info(f"Proveedor: {order_data.get('provider_name')}")
        logger.info(f"Peso: {order_data.get('weight')}g")
        logger.info(f"Prioridad: {order_data.get('priority')}")
        logger.info(f"Fragilidad: {order_data.get('fragility')}")
        logger.info(f"Fecha recogida: {order_data.get('pickup_date')}")
        logger.info("=" * 60)


# ==========================================
# SUJETO (Subject/Observable)
# ==========================================

class OrderNotificationSubject:
    """
    Sujeto que mantiene una lista de observadores y los notifica de cambios.
    
    Esta clase es el núcleo del patrón Observer. Mantiene referencias
    a todos los observadores y proporciona métodos para gestionar suscripciones.
    """
    
    def __init__(self):
        """Inicializa el sujeto con una lista vacía de observadores."""
        self._observers: List[OrderObserver] = []
    
    def attach(self, observer: OrderObserver) -> None:

        if observer not in self._observers:
            self._observers.append(observer)
            logger.debug(f"Observador adjuntado: {observer.get_observer_name()}")
        else:
            logger.warning(f"Observador ya estaba adjuntado: {observer.get_observer_name()}")
    
    def detach(self, observer: OrderObserver) -> None:
        try:
            self._observers.remove(observer)
            logger.debug(f"Observador desadjuntado: {observer.get_observer_name()}")
        except ValueError:
            logger.warning(f"Observador no encontrado: {observer.get_observer_name()}")
    
    def notify(self, order_data: Dict[str, Any]) -> None:

        logger.info(f"📢 Notificando a {len(self._observers)} observadores...")
        
        for observer in self._observers:
            try:
                observer.update(order_data)
            except Exception as e:
                # No fallar si un observador falla
                logger.error(f"Error en {observer.get_observer_name()}: {e}")
    
    def get_observers_count(self) -> int:
        return len(self._observers)
    
    def get_observers_names(self) -> List[str]:

        return [obs.get_observer_name() for obs in self._observers]


# ==========================================
# UTILIDADES
# ==========================================

def truncate_message_for_db(message: str, max_length: int = 500) -> str:
    if len(message) <= max_length:
        return message
    
    return message[:max_length - 3] + "..."


# ==========================================
# FACTORY DE OBSERVADORES (Facilita configuración)
# ==========================================

def create_default_observers() -> List[OrderObserver]:
    return [
        EmailNotificationObserver(),
        WebhookNotificationObserver(),
        SMSNotificationObserver(),
        LoggingObserver()
    ]


def create_minimal_observers() -> List[OrderObserver]:

    return [
        LoggingObserver()
    ]
