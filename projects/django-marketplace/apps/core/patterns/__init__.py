"""
Paquete de patrones de diseño del sistema.

Este paquete organiza los patrones de diseño en tres categorías:
- creational: Patrones de creación (Builder)
- structural: Patrones estructurales (Adapter)
- behavioral: Patrones de comportamiento (Strategy, Observer)
"""

# Imports facilitados para uso externo
from .creational.builder import OrderBuilder
from .structural.adapter import (
    ShippingProvider,
    ShippingAdapterFactory
)
from .behavioral.strategy import (
    ProviderSelector,
    StandardSelectionStrategy,
    EcoFriendlySelectionStrategy,
    CostOptimizedSelectionStrategy,
    get_strategy_by_name
)
from .behavioral.observer import (
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
