"""
Script de prueba para demostrar el funcionamiento de los patrones de diseño.

Ejecutar desde el directorio del proyecto:
    python test_patterns.py

Este script demuestra:
- Builder: Construccion paso a paso de pedidos
- Adapter: Integracion con multiples proveedores
- Strategy: Seleccion inteligente segun estrategia
- Observer: Notificaciones multi-canal
"""

import os
import sys
import django
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.core.models import Product, Order, OrderItem, Shipment, Notification
from apps.core.patterns.creacional.builder import OrderBuilder
from apps.core.patterns.estructural.adapter import (
    MotoYAAdapter, EcoBikeAdapter, PaqueteriaZAdapter, ShippingAdapterFactory
)
from apps.core.patterns.comportamental.strategy import (
    ProviderSelector,
    StandardSelectionStrategy,
    EcoFriendlySelectionStrategy,
    CostOptimizedSelectionStrategy
)
from apps.core.patterns.comportamental.observer import (
    OrderNotificationSubject,
    EmailNotificationObserver,
    WebhookNotificationObserver,
    SMSNotificationObserver,
    LoggingObserver
)


def print_header(title: str):
    """Imprime un encabezado bonito."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_section(title: str):
    """Imprime una seccion."""
    print(f"\n--- {title} ---")


def test_builder_pattern():
    """Prueba el patron Builder."""
    print_header("PATRON BUILDER (CREACIONAL)")
    print("Demostracion: Construccion paso a paso de pedidos complejos\n")
    
    # Obtener productos de la BD
    products = list(Product.objects.all()[:3])
    if not products:
        print("ERROR: No hay productos en la base de datos")
        return None
    
    print(f"Productos disponibles para pruebas:")
    for p in products:
        print(f"  - ID {p.id}: {p.name} ({p.weight_grams}g)")
    
    print_section("Escenario 1: Pedido simple")
    builder1 = OrderBuilder()
    order1 = (builder1
              .with_customer('cliente1@test.com')
              .with_address('Calle 123')
              .with_priority('normal')
              .with_fragility('ninguna')
              .with_items({products[0].id: 2})
              .build())
    
    summary1 = builder1.get_order_summary()
    print(f"Cliente: {order1.customer_email}")
    print(f"Codigo paquete: {summary1['package_code']}")
    print(f"Items: 2 x {products[0].name}")
    print(f"Peso total: {summary1['total_weight']}g")
    print(f"Etiqueta manejo: {summary1['handling_label']}")
    print(f"Fecha estimada: {summary1['estimated_pickup_date']}")
    
    print_section("Escenario 2: Pedido fragil y express")
    builder2 = OrderBuilder()
    order2 = (builder2
              .with_customer('cliente2@test.com')
              .with_address('Avenida 456')
              .with_priority('express')
              .with_fragility('alta')
              .with_items({products[0].id: 1, products[1].id: 3})
              .build())
    
    summary2 = builder2.get_order_summary()
    print(f"Cliente: {order2.customer_email}")
    print(f"Codigo paquete: {summary2['package_code']}")
    print(f"Items: 1 x {products[0].name}, 3 x {products[1].name}")
    print(f"Peso total: {summary2['total_weight']}g")
    print(f"Etiqueta manejo: {summary2['handling_label']}")
    print(f"Prioridad: {order2.priority}")
    
    print_section("Escenario 3: Pedido con validacion de items vacios")
    try:
        builder3 = OrderBuilder()
        order3 = (builder3
                  .with_customer('cliente3@test.com')
                  .with_address('Carrera 789')
                  .with_priority('normal')
                  .with_fragility('ninguna')
                  .with_items({})  # Sin items
                  .build())
    except ValueError as e:
        print(f"Validacion correcta: {e}")
    
    print("\nBENEFICIOS DEL PATRON BUILDER:")
    print("- Construccion paso a paso clara y legible")
    print("- Validaciones centralizadas en el builder")
    print("- Generacion automatica de codigos y etiquetas")
    print("- Inmutabilidad del objeto final")
    
    return order1, order2


def test_adapter_pattern():
    """Prueba el patron Adapter."""
    print_header("PATRON ADAPTER (ESTRUCTURAL)")
    print("Demostracion: Integracion uniforme con APIs heterogeneas\n")
    
    print_section("Adaptadores disponibles")
    adapters = [
        ('MotoYA', MotoYAAdapter()),
        ('EcoBike', EcoBikeAdapter()),
        ('PaqueteriaZ', PaqueteriaZAdapter())
    ]
    
    for name, adapter in adapters:
        print(f"\n{name}:")
        print(f"  - Nombre: {adapter.get_provider_name()}")
    
    print_section("Escenario 1: Solicitud a MotoYA")
    motoya = MotoYAAdapter()
    data1 = {
        'order_id': 1001,
        'weight': 2500,
        'priority': 'express',
        'fragility': 'alta',
        'address': 'Calle 123'
    }
    tracking1 = motoya.request_pickup(data1)
    print(f"Datos enviados: Peso={data1['weight']}g, Prioridad={data1['priority']}")
    print(f"Tracking generado: {tracking1}")
    print(f"Proveedor: {motoya.get_provider_name()}")
    
    print_section("Escenario 2: Solicitud a EcoBike")
    ecobike = EcoBikeAdapter()
    data2 = {
        'order_id': 1002,
        'weight': 500,
        'priority': 'normal',
        'fragility': 'ninguna',
        'address': 'Avenida 456'
    }
    tracking2 = ecobike.request_pickup(data2)
    print(f"Datos enviados: Peso={data2['weight']}g, Prioridad={data2['priority']}")
    print(f"Tracking generado: {tracking2}")
    print(f"Proveedor: {ecobike.get_provider_name()}")
    
    print_section("Escenario 3: Solicitud a PaqueteriaZ")
    paqz = PaqueteriaZAdapter()
    data3 = {
        'order_id': 1003,
        'weight': 15000,
        'priority': 'normal',
        'fragility': 'media',
        'address': 'Carrera 789'
    }
    tracking3 = paqz.request_pickup(data3)
    print(f"Datos enviados: Peso={data3['weight']}g, Prioridad={data3['priority']}")
    print(f"Tracking generado: {tracking3}")
    print(f"Proveedor: {paqz.get_provider_name()}")
    
    print_section("Factory: Creacion dinamica de adapters")
    factory_providers = ShippingAdapterFactory.get_available_providers()
    print(f"Proveedores disponibles: {factory_providers}")
    
    for provider in factory_providers:
        adapter = ShippingAdapterFactory.create_adapter(provider)
        print(f"  - {provider}: {adapter.get_provider_name()}")
    
    print("\nBENEFICIOS DEL PATRON ADAPTER:")
    print("- Interfaz uniforme para APIs diferentes")
    print("- Facil agregar nuevos proveedores (OCP)")
    print("- Codigo cliente desacoplado de implementaciones")
    print("- Testeo simplificado con mocks")
    
    return tracking1, tracking2, tracking3


def test_strategy_pattern():
    """Prueba el patron Strategy."""
    print_header("PATRON STRATEGY (COMPORTAMENTAL)")
    print("Demostracion: Seleccion inteligente de proveedores segun algoritmo\n")
    
    available_providers = ['motoya', 'ecobike', 'paqz']
    
    print_section("Escenario 1: Estrategia ESTANDAR")
    strategy1 = StandardSelectionStrategy()
    selector1 = ProviderSelector(strategy1)
    
    data1 = {
        'priority': 'express',
        'fragility': 'alta',
        'weight': 3000,
        'address': 'Centro ciudad'
    }
    selected1 = selector1.select_provider(data1, available_providers)
    print(f"Datos: Priority={data1['priority']}, Fragility={data1['fragility']}, Weight={data1['weight']}g")
    print(f"Proveedor seleccionado: {selected1}")
    print(f"Razon: Express + Fragil -> MotoYA (rapido y cuidadoso)")
    
    print_section("Escenario 2: Estrategia ECOLOGICA")
    strategy2 = EcoFriendlySelectionStrategy()
    selector2 = ProviderSelector(strategy2)
    
    data2 = {
        'priority': 'normal',
        'fragility': 'ninguna',
        'weight': 800,
        'address': 'Zona norte'
    }
    selected2 = selector2.select_provider(data2, available_providers)
    print(f"Datos: Priority={data2['priority']}, Weight={data2['weight']}g")
    print(f"Proveedor seleccionado: {selected2}")
    print(f"Razon: Peso < 5kg -> EcoBike (transporte ecologico)")
    
    print_section("Escenario 3: Estrategia OPTIMIZACION DE COSTO")
    strategy3 = CostOptimizedSelectionStrategy()
    selector3 = ProviderSelector(strategy3)
    
    data3 = {
        'priority': 'normal',
        'fragility': 'ninguna',
        'weight': 12000,
        'address': 'Zona industrial'
    }
    selected3 = selector3.select_provider(data3, available_providers)
    print(f"Datos: Priority={data3['priority']}, Weight={data3['weight']}g")
    print(f"Proveedor seleccionado: {selected3}")
    print(f"Razon: Peso > 10kg -> PaqueteriaZ (economia en volumen)")
    
    print_section("Cambio dinamico de estrategia")
    selector = ProviderSelector(StandardSelectionStrategy())
    print(f"Estrategia inicial: StandardSelectionStrategy")
    
    selector.set_strategy(EcoFriendlySelectionStrategy())
    print(f"Estrategia cambiada: EcoFriendlySelectionStrategy")
    
    selector.set_strategy(CostOptimizedSelectionStrategy())
    print(f"Estrategia cambiada: CostOptimizedSelectionStrategy")
    
    print("\nBENEFICIOS DEL PATRON STRATEGY:")
    print("- Algoritmos intercambiables en tiempo de ejecucion")
    print("- Facil agregar nuevas estrategias (OCP)")
    print("- Elimina condicionales complejos")
    print("- Testing independiente de cada estrategia")
    
    return selected1, selected2, selected3


def test_observer_pattern():
    """Prueba el patron Observer."""
    print_header("PATRON OBSERVER (COMPORTAMENTAL)")
    print("Demostracion: Sistema de notificaciones multi-canal\n")
    
    print_section("Configuracion de observadores")
    subject = OrderNotificationSubject()
    
    email_obs = EmailNotificationObserver()
    webhook_obs = WebhookNotificationObserver()
    sms_obs = SMSNotificationObserver()
    logging_obs = LoggingObserver()
    
    subject.attach(email_obs)
    subject.attach(webhook_obs)
    subject.attach(sms_obs)
    subject.attach(logging_obs)
    
    print(f"Observadores registrados: {len(subject._observers)}")
    print("  - EmailNotificationObserver")
    print("  - WebhookNotificationObserver")
    print("  - SMSNotificationObserver")
    print("  - LoggingObserver")
    
    print_section("Escenario 1: Notificacion de pedido creado")
    data1 = {
        'order_code': 'PKG-00000001',
        'customer_email': 'cliente@test.com',
        'tracking_code': 'MOTOYA-12345',
        'provider_name': 'motoya',
        'pickup_date': '2025-10-11',
        'weight': 2500,
        'priority': 'express',
        'fragility': 'alta',
        'address': 'Calle 123'
    }
    subject.notify(data1)
    
    print_section("Escenario 2: Notificacion de pedido liviano")
    data2 = {
        'order_code': 'PKG-00000002',
        'customer_email': 'cliente2@test.com',
        'tracking_code': 'ECOBIKE-54321',
        'provider_name': 'ecobike',
        'pickup_date': '2025-10-11',
        'weight': 500,
        'priority': 'normal',
        'fragility': 'ninguna',
        'address': 'Avenida 456'
    }
    subject.notify(data2)
    
    print_section("Escenario 3: Desregistrar un observador")
    subject.detach(sms_obs)
    print(f"SMS Observer desregistrado")
    print(f"Observadores activos: {len(subject._observers)}")
    
    data3 = {
        'order_code': 'PKG-00000003',
        'customer_email': 'cliente3@test.com',
        'tracking_code': 'PAQZ-98765',
        'provider_name': 'paqz',
        'pickup_date': '2025-10-11',
        'weight': 15000,
        'priority': 'normal',
        'fragility': 'media',
        'address': 'Carrera 789'
    }
    subject.notify(data3)
    print("Nota: SMS no enviado porque fue desregistrado")
    
    print("\nBENEFICIOS DEL PATRON OBSERVER:")
    print("- Desacoplamiento entre emisor y receptores")
    print("- Facil agregar/remover canales de notificacion")
    print("- Broadcasting automatico a todos los observadores")
    print("- Cada observador implementa su propia logica")
    
    return subject


def test_integration():
    """Prueba integracion de todos los patrones."""
    print_header("INTEGRACION DE PATRONES")
    print("Demostracion: Flujo completo usando los 4 patrones\n")
    
    # Obtener productos
    products = list(Product.objects.all()[:2])
    if not products:
        print("ERROR: No hay productos en la base de datos")
        return
    
    print_section("Paso 1: BUILDER - Construccion del pedido")
    builder = OrderBuilder()
    order = (builder
             .with_customer('integracion@test.com')
             .with_address('Calle Integracion 123')
             .with_priority('express')
             .with_fragility('alta')
             .with_items({products[0].id: 2, products[1].id: 1})
             .build())
    
    summary = builder.get_order_summary()
    print(f"Pedido construido: #{order.id}")
    print(f"Codigo: {summary['package_code']}")
    print(f"Peso: {summary['total_weight']}g")
    
    print_section("Paso 2: STRATEGY - Seleccion de proveedor")
    strategy = StandardSelectionStrategy()
    selector = ProviderSelector(strategy)
    
    selection_data = {
        'priority': order.priority,
        'fragility': order.fragility,
        'weight': order.total_weight,
        'address': order.address
    }
    available_providers = ['motoya', 'ecobike', 'paqz']
    selected_provider = selector.select_provider(selection_data, available_providers)
    print(f"Proveedor seleccionado: {selected_provider}")
    
    print_section("Paso 3: ADAPTER - Integracion con proveedor")
    adapter = ShippingAdapterFactory.create_adapter(selected_provider)
    adapter_data = {
        'order_id': order.id,
        'weight': order.total_weight,
        'priority': order.priority,
        'fragility': order.fragility,
        'address': order.address
    }
    tracking_code = adapter.request_pickup(adapter_data)
    print(f"Tracking generado: {tracking_code}")
    print(f"Proveedor: {adapter.get_provider_name()}")
    
    # Crear envio
    shipment = Shipment.objects.create(
        order=order,
        provider=selected_provider,
        tracking_id=tracking_code,
        status='CONFIRMADO'
    )
    print(f"Envio registrado: #{shipment.id}")
    
    print_section("Paso 4: OBSERVER - Notificaciones multi-canal")
    subject = OrderNotificationSubject()
    observers = [
        EmailNotificationObserver(),
        WebhookNotificationObserver(),
        SMSNotificationObserver(),
        LoggingObserver()
    ]
    
    for observer in observers:
        subject.attach(observer)
    
    notification_data = {
        'order_code': summary['package_code'],
        'customer_email': order.customer_email,
        'tracking_code': tracking_code,
        'provider_name': selected_provider,
        'pickup_date': summary['estimated_pickup_date'],
        'weight': order.total_weight,
        'priority': order.priority,
        'fragility': order.fragility,
        'address': order.address
    }
    subject.notify(notification_data)
    
    # Verificar notificaciones en BD
    notifications = Notification.objects.filter(order_id=order.id)
    print(f"\nNotificaciones registradas: {notifications.count()}")
    for notif in notifications:
        print(f"  - {notif.channel}: {notif.message[:50]}...")
    
    print("\n" + "=" * 80)
    print("RESUMEN DE LA INTEGRACION:")
    print("=" * 80)
    print(f"1. BUILDER: Pedido #{order.id} construido con {summary['total_weight']}g")
    print(f"2. STRATEGY: Proveedor '{selected_provider}' seleccionado")
    print(f"3. ADAPTER: Tracking '{tracking_code}' generado")
    print(f"4. OBSERVER: {notifications.count()} notificaciones enviadas")
    print("\nTODOS LOS PATRONES FUNCIONANDO EN ARMONIA!")


def main():
    """Funcion principal."""
    print("\n" + "=" * 80)
    print("  SCRIPT DE PRUEBA - PATRONES DE DISEÑO")
    print("  Sistema de Pedidos y Entregas")
    print("  Fecha: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 80)
    
    try:
        # Verificar que hay productos
        product_count = Product.objects.count()
        print(f"\nProductos en base de datos: {product_count}")
        
        if product_count == 0:
            print("\nADVERTENCIA: No hay productos. Ejecuta: python manage.py poblar_datos")
            return
        
        # Ejecutar pruebas
        test_builder_pattern()
        input("\nPresiona ENTER para continuar con Adapter...")
        
        test_adapter_pattern()
        input("\nPresiona ENTER para continuar con Strategy...")
        
        test_strategy_pattern()
        input("\nPresiona ENTER para continuar con Observer...")
        
        test_observer_pattern()
        input("\nPresiona ENTER para continuar con Integracion...")
        
        test_integration()
        
        print("\n" + "=" * 80)
        print("  PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("=" * 80)
        
    except KeyboardInterrupt:
        print("\n\nPruebas interrumpidas por el usuario.")
    except Exception as e:
        print(f"\n\nERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
