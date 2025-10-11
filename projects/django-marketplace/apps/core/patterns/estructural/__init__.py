"""
Patrones eestructurales (estructural Patterns).

Estos patrones se enfocan en cómo las clases y objetos se componen
para formar estructuras más grandes.
"""

from .adapter import (
    ShippingProvider,
    MotoYAAdapter,
    EcoBikeAdapter,
    PaqueteriaZAdapter,
    ShippingAdapterFactory
)

__all__ = [
    'ShippingProvider',
    'MotoYAAdapter',
    'EcoBikeAdapter',
    'PaqueteriaZAdapter',
    'ShippingAdapterFactory',
]
