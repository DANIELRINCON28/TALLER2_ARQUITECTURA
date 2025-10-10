"""
Patrón Estructural: Adapter
Responsabilidad: Unificar interfaces heterogéneas de proveedores de envío externos.

El patrón Adapter permite que clases con interfaces incompatibles trabajen juntas,
convirtiendo la interfaz de una clase en otra que los clientes esperan.
"""
import secrets
from typing import Dict, List, Any, Protocol


# ==========================================
# INTERFAZ COMÚN (TARGET)
# ==========================================

class ShippingProvider(Protocol):
    """
    Interfaz común para todos los proveedores de envío.
    Define el contrato que deben cumplir todos los adapters.
    
    Esta es la interfaz que el cliente (OrderService) espera usar,
    independientemente del proveedor real.
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


# ==========================================
# ADAPTEES (Servicios externos con APIs propias)
# ==========================================

class MotoYAProvider:
    """
    Clase que simula la API específica de MotoYA.
    Representa un servicio externo con su propia interfaz.
    
    En un escenario real, esta sería una librería de terceros
    o un cliente HTTP que consume su API REST.
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


# ==========================================
# ADAPTERS (Adaptadores que implementan la interfaz común)
# ==========================================

class MotoYAAdapter:
    """
    Adapter para MotoYA que implementa la interfaz común ShippingProvider.
    Traduce las llamadas de la interfaz común a la API específica de MotoYA.
    
    Ventajas:
    - Permite usar MotoYA sin modificar su API original
    - Encapsula la complejidad de la conversión de datos
    - Facilita el cambio de proveedor sin afectar el código cliente
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


# ==========================================
# FACTORY (Patrón adicional para crear adapters)
# ==========================================

class ShippingAdapterFactory:
    """
    Factory para crear adapters de proveedores de envío.
    Encapsula la creación de adapters y permite fácil extensión.
    
    Ventajas:
    - Centraliza la lógica de creación de adapters
    - Facilita agregar nuevos proveedores sin modificar código cliente
    - Proporciona un punto único de configuración
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
    
    @classmethod
    def register_provider(cls, name: str, adapter_class):
        """
        Registra un nuevo proveedor dinámicamente.
        Permite extensibilidad sin modificar el código existente (OCP).
        
        Args:
            name: Nombre del proveedor
            adapter_class: Clase del adapter
        """
        cls._adapters[name.lower()] = adapter_class
