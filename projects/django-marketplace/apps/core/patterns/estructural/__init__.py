"""
Patrones estructurales (Structural Patterns).

Estos patrones se enfocan en como las clases y objetos se componen
para formar estructuras mas grandes.
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
