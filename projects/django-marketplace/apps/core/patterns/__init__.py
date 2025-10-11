"""
Paquete de patrones de diseño del sistema.

Este paquete organiza los patrones de diseño en tres categorías:
- creacional: Patrones de creación (Builder)
- estructural: Patrones eestructurales (Adapter)
- comportamental: Patrones de comportamiento (Strategy, Observer)
"""

# Imports facilitados para uso externo
from .creacional.builder import OrderBuilder
from .estructural.adapter import (
    ShippingProvider,
    ShippingAdapterFactory
)
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
