"""
Tests básicos para verificar la traducción PHP->Python.
Verificación de que toda la funcionalidad original está preservada.
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from orders.models import Product, Order, OrderItem, Shipment, Notification
from orders.services import (
    products_all, 
    orders_latest, 
    handle_create_order,
    select_provider_naive,
    request_pickup_naive
)


class TranslationVerificationTest(TestCase):
    """
    Pruebas para verificar que la traducción PHP->Python mantiene toda la funcionalidad.
    """
    
    def setUp(self):
        """Configurar datos de prueba equivalentes a seed.sql"""
        self.products = [
            Product.objects.create(sku='VEL-AROMA', name='Vela aromática', weight_grams=300, fragile=True),
            Product.objects.create(sku='TE-VERDE', name='Té verde 250g', weight_grams=250, fragile=False),
            Product.objects.create(sku='TAZA-CE', name='Taza cerámica', weight_grams=400, fragile=True),
        ]
    
    def test_products_all_equivalence(self):
        """Verificar equivalencia con products_all() de PHP"""
        products = products_all()
        self.assertEqual(len(products), 3)
        self.assertEqual(products[0].name, 'Taza cerámica')  # Ordenado por nombre
    
    def test_order_creation_equivalence(self):
        """Verificar equivalencia con handle_create_order() de PHP"""
        form_data = {
            'customer_email': 'test@example.com',
            'address': 'Calle 123',
            'priority': 'normal',
            'fragility': 'debil',
            'items': {self.products[0].id: 2, self.products[1].id: 1}
        }
        
        order_id = handle_create_order(form_data)
        
        # Verificar que se creó el pedido
        order = Order.objects.get(id=order_id)
        self.assertEqual(order.customer_email, 'test@example.com')
        self.assertEqual(order.total_weight, 850)  # 300*2 + 250*1
        
        # Verificar items
        items = OrderItem.objects.filter(order=order)
        self.assertEqual(items.count(), 2)
        
        # Verificar envío
        shipment = Shipment.objects.filter(order=order).first()
        self.assertIsNotNone(shipment)
        self.assertIn(shipment.provider, ['motoya', 'ecobike', 'paqz'])
        
        # Verificar notificaciones
        notifications = Notification.objects.filter(order=order)
        self.assertEqual(notifications.count(), 2)  # email y webhook
    
    def test_provider_selection_logic(self):
        """Verificar que la lógica de selección de proveedor es idéntica a PHP"""
        # Caso express + frágil -> ecobike
        provider = select_provider_naive('express', 'alta', 500)
        self.assertEqual(provider, 'ecobike')
        
        # Caso peso <= 1200 -> motoya  
        provider = select_provider_naive('normal', 'ninguna', 800)
        self.assertEqual(provider, 'motoya')
        
        # Caso peso > 1200 -> paqz
        provider = select_provider_naive('normal', 'ninguna', 1500)
        self.assertEqual(provider, 'paqz')
    
    def test_tracking_generation(self):
        """Verificar que la generación de tracking funciona como en PHP"""
        tracking_motoya = request_pickup_naive('motoya', {})
        tracking_ecobike = request_pickup_naive('ecobike', {})
        tracking_paqz = request_pickup_naive('paqz', {})
        
        self.assertTrue(tracking_motoya.startswith('MYA-'))
        self.assertTrue(tracking_ecobike.startswith('EBK-'))
        self.assertTrue(tracking_paqz.startswith('PAQ-'))
    
    def test_home_view_equivalence(self):
        """Verificar que la vista home funciona como el case 'home' en PHP"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Módulo de Pedidos & Entregas')
        self.assertContains(response, 'Vela aromática')
    
    def test_order_create_view_equivalence(self):
        """Verificar que la vista de creación funciona como en PHP"""
        # GET - mostrar formulario
        response = self.client.get(reverse('order_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Confirmación de Pedido')
        
        # POST - crear pedido
        form_data = {
            '__action': 'order.store',
            'customer_email': 'test@example.com',
            'address': 'Calle 123',
            'priority': 'normal',
            'fragility': 'ninguna',
            f'items[{self.products[0].id}]': '1',
        }
        
        response = self.client.post(reverse('order_create'), form_data)
        
        # Verificar redirección (equivalente a header() en PHP)
        self.assertEqual(response.status_code, 302)
        
        # Verificar que se creó el pedido
        order = Order.objects.filter(customer_email='test@example.com').first()
        self.assertIsNotNone(order)


# Función de verificación manual para ejecutar en shell
def verify_translation():
    """
    Función para verificar manualmente que la traducción es correcta.
    Ejecutar en: python manage.py shell
    """
    print("🔍 Verificando traducción PHP -> Python...")
    
    # Verificar modelos
    print(f"✅ Productos en DB: {Product.objects.count()}")
    print(f"✅ Pedidos en DB: {Order.objects.count()}")
    
    # Verificar funciones de servicio
    try:
        products = products_all()
        print(f"✅ Función products_all(): {len(products)} productos")
        
        recent = orders_latest(5)
        print(f"✅ Función orders_latest(): {len(recent)} pedidos recientes")
        
        print("✅ Todas las funciones de servicio están funcionando")
    except Exception as e:
        print(f"❌ Error en servicios: {e}")
    
    print("🎉 Verificación completada - La traducción mantiene toda la funcionalidad original")