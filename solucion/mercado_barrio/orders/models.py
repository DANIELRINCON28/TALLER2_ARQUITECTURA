"""
Modelos de datos para la aplicación de mercado barrio.
Traducción directa del schema SQL (schema.sql) a modelos Django ORM.
Migrado de MySQL a PostgreSQL manteniendo la misma estructura y funcionalidad.
"""
from django.db import models
from django.utils import timezone
from django.core.validators import EmailValidator
import secrets


class Product(models.Model):
    """
    Modelo de productos.
    Traducción directa de la tabla 'products' en schema.sql.
    """
    # Equivalente a: id INT AUTO_INCREMENT PRIMARY KEY
    # Django lo crea automáticamente como 'id'
    
    # Equivalente a: sku VARCHAR(50) NOT NULL UNIQUE
    sku = models.CharField(max_length=50, unique=True, null=False)
    
    # Equivalente a: name VARCHAR(100) NOT NULL
    name = models.CharField(max_length=100, null=False)
    
    # Equivalente a: weight_grams INT NOT NULL DEFAULT 0
    weight_grams = models.IntegerField(default=0, null=False)
    
    # Equivalente a: fragile TINYINT(1) NOT NULL DEFAULT 0
    fragile = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = 'products'
        ordering = ['name']  # Equivalente a ORDER BY name ASC en products_all()

    def __str__(self):
        return f"{self.name} ({self.weight_grams}g)"


class Order(models.Model):
    """
    Modelo de pedidos.
    Traducción directa de la tabla 'orders' en schema.sql.
    """
    # Opciones de prioridad - equivalente a ENUM('normal','express')
    PRIORITY_CHOICES = [
        ('normal', 'Normal'),
        ('express', 'Express'),
    ]
    
    # Opciones de fragilidad - equivalente a ENUM('ninguna','debil','alta')
    FRAGILITY_CHOICES = [
        ('ninguna', 'Ninguna'),
        ('debil', 'Débil'),
        ('alta', 'Alta'),
    ]
    
    # Equivalente a: customer_email VARCHAR(120) NOT NULL
    customer_email = models.EmailField(max_length=120, null=False, validators=[EmailValidator()])
    
    # Equivalente a: address VARCHAR(200) NOT NULL
    address = models.CharField(max_length=200, null=False)
    
    # Equivalente a: priority ENUM('normal','express') NOT NULL DEFAULT 'normal'
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal', null=False)
    
    # Equivalente a: fragility ENUM('ninguna','debil','alta') NOT NULL DEFAULT 'ninguna'
    fragility = models.CharField(max_length=10, choices=FRAGILITY_CHOICES, default='ninguna', null=False)
    
    # Equivalente a: total_weight INT NOT NULL DEFAULT 0
    total_weight = models.IntegerField(default=0, null=False)
    
    # Equivalente a: created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'orders'
        ordering = ['-id']  # Equivalente a ORDER BY id DESC en orders_latest()

    def __str__(self):
        return f"Pedido #{self.id} - {self.customer_email}"


class OrderItem(models.Model):
    """
    Modelo de items de pedido.
    Traducción directa de la tabla 'order_items' en schema.sql.
    """
    # Equivalente a: order_id INT NOT NULL con FOREIGN KEY
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False)
    
    # Equivalente a: product_id INT NOT NULL con FOREIGN KEY
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, null=False)
    
    # Equivalente a: quantity INT NOT NULL
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
    # Opciones de estado - equivalente a ENUM('CONFIRMADO','DESPACHADO','EN_RUTA','ENTREGADO')
    STATUS_CHOICES = [
        ('CONFIRMADO', 'Confirmado'),
        ('DESPACHADO', 'Despachado'),
        ('EN_RUTA', 'En Ruta'),
        ('ENTREGADO', 'Entregado'),
    ]
    
    # Equivalente a: order_id INT NOT NULL con FOREIGN KEY
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False)
    
    # Equivalente a: provider VARCHAR(30) NOT NULL
    provider = models.CharField(max_length=30, null=False)
    
    # Equivalente a: tracking_id VARCHAR(60) NOT NULL
    tracking_id = models.CharField(max_length=60, null=False)
    
    # Equivalente a: status ENUM(...) NOT NULL DEFAULT 'CONFIRMADO'
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='CONFIRMADO', null=False)
    
    # Equivalente a: created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shipments'
        ordering = ['-id']  # Para obtener el más reciente en shipment_by_order()

    def __str__(self):
        return f"{self.provider} - {self.tracking_id} (Pedido #{self.order.id})"


class Notification(models.Model):
    """
    Modelo de notificaciones.
    Traducción directa de la tabla 'notifications' en schema.sql.
    """
    # Equivalente a: order_id INT NOT NULL con FOREIGN KEY
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False)
    
    # Equivalente a: channel VARCHAR(20) NOT NULL
    channel = models.CharField(max_length=20, null=False)
    
    # Equivalente a: message VARCHAR(255) NOT NULL
    message = models.CharField(max_length=255, null=False)
    
    # Equivalente a: created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'notifications'

    def __str__(self):
        return f"{self.channel}: {self.message[:50]}... (Pedido #{self.order.id})"