"""
Patrones de comportamiento (Behavioral Patterns).

Estos patrones se enfocan en la comunicación entre objetos,
cómo los objetos interactúan y distribuyen responsabilidades.
"""

from .strategy import (
    ProviderSelectionStrategy,
    StandardSelectionStrategy,
    EcoFriendlySelectionStrategy,
    CostOptimizedSelectionStrategy,
    WeightBasedSelectionStrategy,
    ProviderSelector,
    get_strategy_by_name,
    STRATEGY_REGISTRY
)

from .observer import (
    OrderObserver,
    EmailNotificationObserver,
    WebhookNotificationObserver,
    SMSNotificationObserver,
    LoggingObserver,
    OrderNotificationSubject,
    create_default_observers,
    create_minimal_observers,
    truncate_message_for_db
)

__all__ = [
    # Strategy
    'ProviderSelectionStrategy',
    'StandardSelectionStrategy',
    'EcoFriendlySelectionStrategy',
    'CostOptimizedSelectionStrategy',
    'WeightBasedSelectionStrategy',
    'ProviderSelector',
    'get_strategy_by_name',
    'STRATEGY_REGISTRY',
    
    # Observer
    'OrderObserver',
    'EmailNotificationObserver',
    'WebhookNotificationObserver',
    'SMSNotificationObserver',
    'LoggingObserver',
    'OrderNotificationSubject',
    'create_default_observers',
    'create_minimal_observers',
    'truncate_message_for_db',
]
