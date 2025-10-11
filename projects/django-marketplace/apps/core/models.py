from django.db import models
from django.utils import timezone
from django.core.validators import EmailValidator
import secrets


class Product(models.Model):
    """
    Modelo de productos.
    Traducción directa de la tabla 'products' en schema.sql.
    """
    sku = models.CharField(max_length=50, unique=True, null=False)
    name = models.CharField(max_length=100, null=False)
    weight_grams = models.IntegerField(default=0, null=False)  
    fragile = models.BooleanField(default=False, null=False)
    class Meta:
        db_table = 'products'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.weight_grams}g)"

class Order(models.Model):
    """
    Modelo de pedidos.
    Traducción directa de la tabla 'orders' en schema.sql.
    """
    PRIORITY_CHOICES = [
        ('normal', 'Normal'),
        ('express', 'Express'),
    ]
    
    FRAGILITY_CHOICES = [
        ('ninguna', 'Ninguna'),
        ('debil', 'Débil'),
        ('alta', 'Alta'),
    ]
    
    customer_email = models.EmailField(max_length=120, null=False, validators=[EmailValidator()])
    address = models.CharField(max_length=200, null=False)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal', null=False)
    fragility = models.CharField(max_length=10, choices=FRAGILITY_CHOICES, default='ninguna', null=False)
    total_weight = models.IntegerField(default=0, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = 'orders'
        ordering = ['-id']

    def __str__(self):
        return f"Pedido #{self.id} - {self.customer_email}"

class OrderItem(models.Model):
    """
    Modelo de items de pedido.
    Traducción directa de la tabla 'order_items' en schema.sql.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, null=False)
    quantity = models.IntegerField(null=False)
    class Meta:
        db_table = 'order_items'

    def __str__(self):
        return f"{self.product.name} x {self.quantity} (Pedido #{self.order.id})"


class Shipment(models.Model):
    """
    Modelo de envíos.
    Traducción directa de la tabla 'shipments' en schema.sql.
    """
    STATUS_CHOICES = [
        ('CONFIRMADO', 'Confirmado'),
        ('DESPACHADO', 'Despachado'),
        ('EN_RUTA', 'En Ruta'),
        ('ENTREGADO', 'Entregado'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False)
    provider = models.CharField(max_length=30, null=False)
    tracking_id = models.CharField(max_length=60, null=False)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='CONFIRMADO', null=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shipments'
        ordering = ['-id'] 

    def __str__(self):
        return f"{self.provider} - {self.tracking_id} (Pedido #{self.order.id})"

class Notification(models.Model):
    """
    Modelo de notificaciones.
    Traducción directa de la tabla 'notifications' en schema.sql.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False)
    channel = models.CharField(max_length=20, null=False)
    message = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'notifications'

    def __str__(self):
        return f"{self.channel}: {self.message[:50]}... (Pedido #{self.order.id})"