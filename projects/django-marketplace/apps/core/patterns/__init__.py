"""
Paquete de patrones de diseno del sistema.

Este paquete organiza los patrones de diseno en tres categorias:
- creacional: Patrones de creacion (Builder)
- estructural: Patrones estructurales (Adapter)
- comportamental: Patrones de comportamiento (Strategy, Observer)
"""

# Imports facilitados para uso externo
from .creacional.builder import OrderBuilder
from .estructural.adapter import ShippingProvider, ShippingAdapterFactory
from .comportamental.strategy import (
    ProviderSelector,
    StandardSelectionStrategy,
    EcoFriendlySelectionStrategy,
    CostOptimizedSelectionStrategy,
    get_strategy_by_name
)
from .comportamental.observer import (
    OrderNotificationSubject,
    EmailNotificationObserver,
    WebhookNotificationObserver,
    SMSNotificationObserver,
    LoggingObserver,
    create_default_observers
)

__all__ = [
    # Builder
    'OrderBuilder',
    
    # Adapter
    'ShippingProvider',
    'ShippingAdapterFactory',
    
    # Strategy
    'ProviderSelector',
    'StandardSelectionStrategy',
    'EcoFriendlySelectionStrategy',
    'CostOptimizedSelectionStrategy',
    'get_strategy_by_name',
    
    # Observer
    'OrderNotificationSubject',
    'EmailNotificationObserver',
    'WebhookNotificationObserver',
    'SMSNotificationObserver',
    'LoggingObserver',
    'create_default_observers',
]
