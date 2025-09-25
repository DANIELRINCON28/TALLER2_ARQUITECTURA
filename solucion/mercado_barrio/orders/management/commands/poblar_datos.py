"""
Comando Django para poblar la base de datos con datos de ejemplo.
Uso: python manage.py poblar_datos
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from mercado_barrio.orders.models import Product, Order, OrderItem, Shipment, Notification
from django.utils import timezone
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Pobla la base de datos con datos de ejemplo para demostrar los patrones de diseño'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limpiar',
            action='store_true',
            help='Limpia los datos existentes antes de insertar nuevos',
        )

    def handle(self, *args, **options):
        self.stdout.write("🗄️  POBLANDO BASE DE DATOS CON DATOS DE EJEMPLO")
        self.stdout.write("=" * 60)

        if options['limpiar']:
            self.limpiar_datos()

        with transaction.atomic():
            self.crear_productos()
            self.crear_pedidos()
            self.crear_envios()
            self.crear_notificaciones()

        self.mostrar_resumen()

    def limpiar_datos(self):
        """Limpia todos los datos existentes."""
        self.stdout.write("🧹 Limpiando datos existentes...")
        
        Notification.objects.all().delete()
        Shipment.objects.all().delete()
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Product.objects.all().delete()
        
        self.stdout.write("   ✅ Datos limpiados")

    def crear_productos(self):
        """Crea productos de ejemplo."""
        self.stdout.write("📦 Creando productos...")
        
        productos = [
            # Productos ligeros y no frágiles
            ('SKU001', 'Arroz Diana 500g', 500, False),
            ('SKU002', 'Aceite Gourmet 250ml', 300, False),
            ('SKU003', 'Sal refinada 500g', 500, False),
            ('SKU004', 'Azúcar blanca 1kg', 1000, False),
            ('SKU005', 'Pasta Doria 500g', 500, False),
            
            # Productos medianos
            ('SKU006', 'Detergente Ariel 1kg', 1100, False),
            ('SKU007', 'Jabón en polvo 2kg', 2000, False),
            ('SKU008', 'Champú Sedal 400ml', 450, False),
            ('SKU009', 'Atún Van Camps 3 latas', 750, False),
            ('SKU010', 'Leche en polvo Klim 400g', 400, False),
            
            # Productos pesados
            ('SKU011', 'Aceite motor 4 litros', 4000, False),
            ('SKU012', 'Detergente líquido 5L', 5200, False),
            ('SKU013', 'Bulto arroz 5kg', 5000, False),
            ('SKU014', 'Caja cerveza 24 unidades', 6000, False),
            ('SKU015', 'Aceite cocina 1 galón', 3800, False),
            
            # Productos frágiles ligeros
            ('SKU016', 'Copas vino cristal (6 und)', 800, True),
            ('SKU017', 'Platos porcelana (4 und)', 1200, True),
            ('SKU018', 'Bombillos LED (10 und)', 300, True),
            ('SKU019', 'Floreros vidrio decorativo', 900, True),
            ('SKU020', 'Vasos cristal (12 und)', 600, True),
            
            # Productos frágiles pesados
            ('SKU021', 'Vajilla completa 50 piezas', 4500, True),
            ('SKU022', 'Espejo decorativo grande', 3200, True),
            ('SKU023', 'Lámpara mesa cristal', 2800, True),
            ('SKU024', 'Set copas champagne (24)', 3600, True),
            ('SKU025', 'Adornos navideños vidrio', 2200, True),
            
            # Productos especiales
            ('SKU026', 'Laptop Gaming', 1800, True),
            ('SKU027', 'Microondas pequeño', 8000, False),
            ('SKU028', 'Cafetera express', 3500, True),
            ('SKU029', 'Ventilador mesa', 2500, False),
            ('SKU030', 'Radio portátil bluetooth', 400, True),
        ]
        
        for sku, name, weight, fragile in productos:
            Product.objects.create(
                sku=sku,
                name=name,
                weight_grams=weight,
                fragile=fragile
            )
        
        self.stdout.write(f"   ✅ {len(productos)} productos creados")

    def crear_pedidos(self):
        """Crea pedidos de ejemplo."""
        self.stdout.write("🛒 Creando pedidos...")
        
        pedidos_data = [
            # Pedidos normales ligeros
            ('cliente1@mercadobarrio.com', 'Carrera 15 #93-47, Bogotá', 'normal', 'ninguna', 1300, 2),
            ('cliente2@mercadobarrio.com', 'Calle 72 #10-34, Medellín', 'normal', 'ninguna', 800, 1),
            ('cliente3@mercadobarrio.com', 'Avenida Santander #45-67, Cali', 'normal', 'debil', 1500, 1),
            
            # Pedidos express frágiles
            ('cliente4@mercadobarrio.com', 'Transversal 8 #12-90, Barranquilla', 'express', 'alta', 2400, 1),
            ('cliente5@mercadobarrio.com', 'Diagonal 25 #34-12, Cartagena', 'express', 'alta', 1800, 1),
            
            # Pedidos pesados
            ('cliente6@mercadobarrio.com', 'Calle Real #67-89, Bucaramanga', 'normal', 'ninguna', 9200, 3),
            ('cliente7@mercadobarrio.com', 'Avenida Principal #23-45, Pereira', 'normal', 'debil', 7800, 2),
            
            # Pedidos mixtos
            ('cliente8@mercadobarrio.com', 'Carrera 50 #28-14, Manizales', 'express', 'debil', 3200, 1),
            ('cliente9@mercadobarrio.com', 'Calle 80 #15-32, Ibagué', 'normal', 'alta', 4500, 1),
            ('cliente10@mercadobarrio.com', 'Avenida Boyacá #45-78, Santa Marta', 'express', 'ninguna', 2800, 1),
        ]
        
        products = list(Product.objects.all())
        
        for email, address, priority, fragility, weight, hours_ago in pedidos_data:
            order = Order.objects.create(
                customer_email=email,
                address=address,
                priority=priority,
                fragility=fragility,
                total_weight=weight,
                created_at=timezone.now() - timedelta(hours=hours_ago)
            )
            
            # Crear items aleatorios para cada pedido
            self.crear_items_pedido(order, weight)
        
        self.stdout.write(f"   ✅ {len(pedidos_data)} pedidos creados")

    def crear_items_pedido(self, order, target_weight):
        """Crea items para un pedido específico."""
        products = list(Product.objects.all())
        current_weight = 0
        items_created = 0
        
        while current_weight < target_weight * 0.8 and items_created < 5:  # Hasta 80% del peso objetivo
            product = random.choice(products)
            quantity = random.randint(1, 3)
            
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )
            
            current_weight += product.weight_grams * quantity
            items_created += 1

    def crear_envios(self):
        """Crea envíos para los pedidos."""
        self.stdout.write("🚚 Creando envíos...")
        
        orders = Order.objects.all()
        providers = ['motoya', 'ecobike', 'paqz']
        statuses = ['CONFIRMADO', 'DESPACHADO', 'EN_RUTA', 'ENTREGADO']
        
        for i, order in enumerate(orders):
            # Seleccionar proveedor basado en las características del pedido
            if order.priority == 'express' and order.fragility == 'alta':
                provider = 'ecobike'
            elif order.total_weight <= 1200:
                provider = 'motoya'
            else:
                provider = 'paqz'
            
            # Generar tracking ID
            tracking_prefixes = {'motoya': 'MYA', 'ecobike': 'EBK', 'paqz': 'PAQ'}
            tracking_id = f"{tracking_prefixes[provider]}-{random.randint(100000, 999999)}"
            
            # Status aleatorio pero lógico
            status = random.choice(statuses)
            
            Shipment.objects.create(
                order=order,
                provider=provider,
                tracking_id=tracking_id,
                status=status,
                created_at=order.created_at + timedelta(minutes=5)
            )
        
        self.stdout.write(f"   ✅ {orders.count()} envíos creados")

    def crear_notificaciones(self):
        """Crea notificaciones de ejemplo."""
        self.stdout.write("🔔 Creando notificaciones...")
        
        orders = Order.objects.all()
        channels = ['email', 'webhook', 'sms']
        
        notifications_count = 0
        for order in orders:
            shipment = Shipment.objects.filter(order=order).first()
            if shipment:
                # Notificación de confirmación
                for channel in channels:
                    message = f"Pedido #{order.id} confirmado y asignado a {shipment.provider} ({shipment.tracking_id})"
                    if channel == 'sms':
                        message = f"Pedido #{order.id} confirmado"
                    
                    Notification.objects.create(
                        order=order,
                        channel=channel,
                        message=message,
                        created_at=order.created_at + timedelta(minutes=10)
                    )
                    notifications_count += 1
                
                # Notificaciones adicionales para algunos estados
                if shipment.status in ['DESPACHADO', 'EN_RUTA', 'ENTREGADO']:
                    Notification.objects.create(
                        order=order,
                        channel='email',
                        message=f"Pedido #{order.id} actualizado: {shipment.status}",
                        created_at=order.created_at + timedelta(hours=1)
                    )
                    notifications_count += 1
        
        self.stdout.write(f"   ✅ {notifications_count} notificaciones creadas")

    def mostrar_resumen(self):
        """Muestra un resumen de los datos creados."""
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("🎉 BASE DE DATOS POBLADA EXITOSAMENTE")
        self.stdout.write("=" * 60)
        
        products_count = Product.objects.count()
        orders_count = Order.objects.count()
        items_count = OrderItem.objects.count()
        shipments_count = Shipment.objects.count()
        notifications_count = Notification.objects.count()
        
        self.stdout.write(f"📦 Productos: {products_count}")
        self.stdout.write(f"🛒 Pedidos: {orders_count}")
        self.stdout.write(f"📋 Items de pedido: {items_count}")
        self.stdout.write(f"🚚 Envíos: {shipments_count}")
        self.stdout.write(f"🔔 Notificaciones: {notifications_count}")
        
        self.stdout.write("\n🚀 LISTO PARA EJECUTAR:")
        self.stdout.write("   python demo_patrones.py")
        self.stdout.write("   python verificar_patrones.py")
        
        # Mostrar algunos ejemplos
        self.stdout.write("\n📊 EJEMPLOS DE DATOS CREADOS:")
        
        # Productos por tipo
        fragiles = Product.objects.filter(fragile=True).count()
        self.stdout.write(f"   🔸 Productos frágiles: {fragiles}")
        self.stdout.write(f"   🔸 Productos normales: {products_count - fragiles}")
        
        # Pedidos por prioridad
        express = Order.objects.filter(priority='express').count()
        self.stdout.write(f"   🔸 Pedidos express: {express}")
        self.stdout.write(f"   🔸 Pedidos normales: {orders_count - express}")
        
        # Envíos por proveedor
        for provider in ['motoya', 'ecobike', 'paqz']:
            count = Shipment.objects.filter(provider=provider).count()
            self.stdout.write(f"   🔸 Envíos {provider}: {count}")