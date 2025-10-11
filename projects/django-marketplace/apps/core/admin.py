"""
Configuración del panel de administración Django.
Equivalente a phpMyAdmin para gestionar la base de datos en el proyecto PHP.
"""
from django.contrib import admin
from .models import Product, Order, OrderItem, Shipment, Notification


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Administración de productos en el panel de Django.
    Equivalente a gestionar la tabla 'products' en phpMyAdmin.
    """
    list_display = ['sku', 'name', 'weight_grams', 'fragile']
    list_filter = ['fragile']
    search_fields = ['sku', 'name']
    ordering = ['name']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Administración de pedidos en el panel de Django.
    Equivalente a gestionar la tabla 'orders' en phpMyAdmin.
    """
    list_display = ['id', 'customer_email', 'priority', 'fragility', 'total_weight', 'created_at']
    list_filter = ['priority', 'fragility', 'created_at']
    search_fields = ['customer_email', 'address']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Administración de items de pedido en el panel de Django.
    Equivalente a gestionar la tabla 'order_items' en phpMyAdmin.
    """
    list_display = ['order', 'product', 'quantity']
    list_filter = ['product']
    autocomplete_fields = ['order', 'product']


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    """
    Administración de envíos en el panel de Django.
    Equivalente a gestionar la tabla 'shipments' en phpMyAdmin.
    """
    list_display = ['order', 'provider', 'tracking_id', 'status', 'created_at']
    list_filter = ['provider', 'status', 'created_at']
    search_fields = ['tracking_id', 'order__customer_email']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Administración de notificaciones en el panel de Django.
    Equivalente a gestionar la tabla 'notifications' en phpMyAdmin.
    """
    list_display = ['order', 'channel', 'message', 'created_at']
    list_filter = ['channel', 'created_at']
    search_fields = ['message', 'order__customer_email']
    ordering = ['-created_at']
    readonly_fields = ['created_at']