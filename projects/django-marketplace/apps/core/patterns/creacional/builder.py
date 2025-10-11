import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Any
from django.db import transaction
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from apps.core.models import Product, Order, OrderItem


class OrderBuilder:
    """
    Builder para la construcción compleja de pedidos.
    Encapsula la lógica de validación, cálculo de pesos, generación de códigos, etc.
    
    Ventajas:
    - Separa la construcción del objeto de su representación
    - Permite construir objetos paso a paso con validación en cada etapa
    - Facilita la creación de objetos con muchos parámetros opcionales
    - Proporciona control sobre el proceso de construcción
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

        email = email.strip()
        try:
            validate_email(email)
            self._customer_email = email
            return self
        except ValidationError:
            raise ValueError('Email inválido')
    
    def with_address(self, address: str) -> 'OrderBuilder':

        address = address.strip()
        if not address:
            raise ValueError('Dirección requerida')
        self._address = address
        return self
    
    def with_priority(self, priority: str) -> 'OrderBuilder':

        self._priority = priority if priority in ['normal', 'express'] else 'normal'
        return self
    
    def with_fragility(self, fragility: str) -> 'OrderBuilder':

        valid_options = ['ninguna', 'debil', 'alta']
        self._fragility = fragility if fragility in valid_options else 'ninguna'
        return self
    
    def with_items(self, items: Dict[str, int]) -> 'OrderBuilder':

        self._items = items
        self._resolve_items()
        return self
    
    def _resolve_items(self):

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
