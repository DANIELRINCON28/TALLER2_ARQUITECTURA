from abc import ABC, abstractmethod
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


# ==========================================
# INTERFAZ OBSERVER (Subscriber)
# ==========================================

class OrderObserver(ABC):
    """
    Interfaz abstracta para observadores de pedidos.
    Define el contrato que todos los observadores concretos deben cumplir.
    
    Ventajas:
    - Desacopla el sujeto (Order) de sus observadores
    - Permite agregar nuevos observadores sin modificar el sujeto
    - Facilita notificaciones a múltiples sistemas de forma consistente
    """
    
    @abstractmethod
    def update(self, order_data: Dict[str, Any]) -> None:
        """
        Método llamado cuando el sujeto notifica un cambio.
        
        Args:
            order_data: Datos del pedido que cambió
        """
        pass
    
    def get_observer_name(self) -> str:
        """
        Obtiene el nombre descriptivo del observador.
        
        Returns:
            Nombre del observador
        """
        return self.__class__.__name__


# ==========================================
# OBSERVADORES CONCRETOS (Concrete Observers)
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
        email_content = self._generate_email_content(order_data)
        
        logger.info(f"📧 Email enviado a {customer_email}")
        logger.info(f"Asunto: Pedido {order_code} confirmado")
        logger.info(f"Tracking: {tracking_code} ({provider_name})")
        logger.debug(f"Contenido: {email_content[:100]}...")
        
    
    def _generate_email_content(self, order_data: Dict[str, Any]) -> str:
        """
        Genera el contenido HTML del email.
        
        Args:
            order_data: Datos del pedido
            
        Returns:
            Contenido HTML del email
        """
        return f"""
        <html>
        <body>
            <h2>¡Pedido Confirmado!</h2>
            <p>Hola {order_data.get('customer_email', 'Cliente')},</p>
            <p>Tu pedido <strong>{order_data.get('order_code')}</strong> ha sido confirmado.</p>
            <p><strong>Código de seguimiento:</strong> {order_data.get('tracking_code')}</p>
            <p><strong>Proveedor:</strong> {order_data.get('provider_name', 'N/A')}</p>
            <p><strong>Fecha de recogida:</strong> {order_data.get('pickup_date')}</p>
            <p>Gracias por tu compra.</p>
        </body>
        </html>
        """


class WebhookNotificationObserver(OrderObserver):
    """
    Observador que envía notificaciones a webhooks externos.
    
    Útil para integración con:
    - Sistemas de terceros (ERP, CRM)
    - Servicios de análisis
    - Plataformas de automatización (Zapier, Make)
    - Microservicios internos
    
    Envía una petición HTTP POST con los datos del pedido.
    """
    
    def __init__(self, webhook_url: str = "https://example.com/webhook"):
        """
        Inicializa el observador con la URL del webhook.
        
        Args:
            webhook_url: URL del endpoint a notificar
        """
        self.webhook_url = webhook_url
    
    def update(self, order_data: Dict[str, Any]) -> None:
        """
        Envía notificación vía webhook cuando se crea un pedido.
        """
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
        """
        Prepara el payload JSON para el webhook.
        
        Args:
            order_data: Datos del pedido
            
        Returns:
            Diccionario con estructura estándar para webhook
        """
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
    """
    Observador que envía notificaciones por SMS.
    
    En producción, integraría con servicios como:
    - Twilio
    - AWS SNS
    - Nexmo/Vonage
    - MessageBird
    
    Ideal para notificaciones urgentes o de alta prioridad.
    """
    
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
        
        # En producción:
        # from twilio.rest import Client
        # client = Client(account_sid, auth_token)
        # client.messages.create(
        #     to=phone_number,
        #     from_="+1234567890",
        #     body=message
        # )
    
    def _extract_phone_number(self, order_data: Dict[str, Any]) -> str:
        """
        Extrae el número de teléfono del pedido.
        
        Args:
            order_data: Datos del pedido
            
        Returns:
            Número de teléfono
        """
        # En un sistema real, esto vendría de la base de datos del cliente
        return "+52 1234567890"  # Simulado
    
    def _generate_sms_message(self, order_data: Dict[str, Any]) -> str:
        """
        Genera el mensaje SMS (máximo 160 caracteres).
        
        Args:
            order_data: Datos del pedido
            
        Returns:
            Mensaje SMS truncado si es necesario
        """
        order_code = order_data.get('order_code', 'N/A')
        tracking_code = order_data.get('tracking_code', 'N/A')
        
        message = f"Pedido {order_code} confirmado. Tracking: {tracking_code}"
        
        # Truncar a 160 caracteres (límite SMS)
        return truncate_message_for_db(message, 160)


class LoggingObserver(OrderObserver):
    """
    Observador que registra eventos en el sistema de logs.
    
    Útil para:
    - Auditoría
    - Debugging
    - Monitoreo de actividad
    - Análisis de métricas
    """
    
    def update(self, order_data: Dict[str, Any]) -> None:
        """
        Registra la creación del pedido en los logs del sistema.
        """
        logger.info("=" * 60)
        logger.info("📦 NUEVO PEDIDO CREADO")
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
    
    Ventajas:
    - Centraliza la lógica de notificación
    - Permite suscripción/desuscripción dinámica
    - Notifica a todos los observadores de forma consistente
    """
    
    def __init__(self):
        """Inicializa el sujeto con una lista vacía de observadores."""
        self._observers: List[OrderObserver] = []
    
    def attach(self, observer: OrderObserver) -> None:
        """
        Adjunta un observador a la lista de suscriptores.
        
        Args:
            observer: Observador a agregar
        """
        if observer not in self._observers:
            self._observers.append(observer)
            logger.debug(f"Observador adjuntado: {observer.get_observer_name()}")
        else:
            logger.warning(f"Observador ya estaba adjuntado: {observer.get_observer_name()}")
    
    def detach(self, observer: OrderObserver) -> None:
        """
        Desadjunta un observador de la lista de suscriptores.
        
        Args:
            observer: Observador a remover
        """
        try:
            self._observers.remove(observer)
            logger.debug(f"Observador desadjuntado: {observer.get_observer_name()}")
        except ValueError:
            logger.warning(f"Observador no encontrado: {observer.get_observer_name()}")
    
    def notify(self, order_data: Dict[str, Any]) -> None:
        """
        Notifica a todos los observadores sobre un cambio.
        
        Args:
            order_data: Datos del pedido a notificar
        """
        logger.info(f"📢 Notificando a {len(self._observers)} observadores...")
        
        for observer in self._observers:
            try:
                observer.update(order_data)
            except Exception as e:
                # No fallar si un observador falla
                logger.error(f"Error en {observer.get_observer_name()}: {e}")
    
    def get_observers_count(self) -> int:
        """
        Obtiene el número de observadores actuales.
        
        Returns:
            Cantidad de observadores suscritos
        """
        return len(self._observers)
    
    def get_observers_names(self) -> List[str]:
        """
        Obtiene los nombres de todos los observadores.
        
        Returns:
            Lista de nombres de observadores
        """
        return [obs.get_observer_name() for obs in self._observers]


# ==========================================
# UTILIDADES
# ==========================================

def truncate_message_for_db(message: str, max_length: int = 500) -> str:
    """
    Trunca un mensaje para almacenamiento en base de datos.
    
    Args:
        message: Mensaje a truncar
        max_length: Longitud máxima permitida
        
    Returns:
        Mensaje truncado con indicador "..." si fue necesario
    """
    if len(message) <= max_length:
        return message
    
    return message[:max_length - 3] + "..."


# ==========================================
# FACTORY DE OBSERVADORES (Facilita configuración)
# ==========================================

def create_default_observers() -> List[OrderObserver]:
    """
    Crea el conjunto estándar de observadores para pedidos.
    
    Returns:
        Lista de observadores configurados por defecto
    """
    return [
        EmailNotificationObserver(),
        WebhookNotificationObserver(),
        SMSNotificationObserver(),
        LoggingObserver()
    ]


def create_minimal_observers() -> List[OrderObserver]:
    """
    Crea un conjunto mínimo de observadores (para testing o desarrollo).
    
    Returns:
        Lista con solo observadores esenciales
    """
    return [
        LoggingObserver()
    ]
