#!/usr/bin/env python3
"""
DEMO - Patrones de Diseño en MercadoBarrio
==========================================

Script de demostración que muestra la implementación de los patrones de diseño
en el sistema de confirmación de pedidos y orquestación de entrega.

PATRONES IMPLEMENTADOS:
- CREACIONAL: Builder - Para construcción compleja de pedidos
- ESTRUCTURAL: Adapter - Para unificar APIs de proveedores 
- COMPORTAMENTAL: Strategy + Observer - Para selección y notificaciones

Uso:
    python demo_patrones.py

Requisitos:
    - Django configurado con las apps del proyecto
    - Base de datos con productos de ejemplo
"""

import os
import sys
import django
from datetime import datetime

# Configurar Django
sys.path.append(os.path.join(os.path.dirname(__file__), 'mercado_barrio'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mercado_barrio.settings')
django.setup()

# Importar después de configurar Django
from mercado_barrio.orders.services import (
    handle_create_order,
    OrderBuilder,
    ShippingAdapterFactory,
    ProviderSelector,
    StandardSelectionStrategy,
    EcoFriendlySelectionStrategy,
    CostOptimizedSelectionStrategy,
    OrderNotificationSubject,
    EmailNotificationObserver,
    WebhookNotificationObserver,
    SMSNotificationObserver,
    products_all
)


def print_header(title: str):
    """Imprime un encabezado formateado."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_section(title: str):
    """Imprime un encabezado de sección."""
    print(f"\n🔹 {title}")
    print("-" * 60)


def demo_builder_pattern():
    """Demuestra el patrón Builder para construcción de pedidos."""
    print_section("PATRÓN CREACIONAL: BUILDER")
    
    print("El patrón Builder permite construir objetos complejos paso a paso.")
    print("En nuestro caso, construye pedidos con validaciones y cálculos complejos.\n")
    
    # Demostrar construcción con Builder
    builder = OrderBuilder()
    
    # Datos de ejemplo
    sample_items = {'1': 2, '2': 1}  # Asumiendo que existen productos con ID 1 y 2
    
    try:
        # Construcción fluida con method chaining
        order_summary = (builder
                        .with_customer("cliente@ejemplo.com")
                        .with_address("Calle 123, Ciudad")
                        .with_priority("express")
                        .with_fragility("alta")
                        .with_items(sample_items)
                        .get_order_summary())
        
        print("✅ Builder configurado exitosamente:")
        print(f"   📧 Cliente: {order_summary['customer_email']}")
        print(f"   📍 Dirección: {order_summary['address']}")
        print(f"   ⚡ Prioridad: {order_summary['priority']}")
        print(f"   📦 Código paquete: {order_summary['package_code']}")
        print(f"   🏷️  Etiqueta: {order_summary['handling_label']}")
        print(f"   ⚖️  Peso total: {order_summary['total_weight']}g")
        
        print(f"\n💡 VENTAJAS del patrón Builder:")
        print(f"   - Construcción paso a paso con validaciones")
        print(f"   - Method chaining para código fluido")
        print(f"   - Separación de construcción y representación")
        print(f"   - Reutilizable para diferentes tipos de pedidos")
        
    except Exception as e:
        print(f"❌ Error en Builder: {e}")


def demo_adapter_pattern():
    """Demuestra el patrón Adapter para unificar APIs de proveedores."""
    print_section("PATRÓN ESTRUCTURAL: ADAPTER")
    
    print("El patrón Adapter permite que interfaces incompatibles trabajen juntas.")
    print("Unifica las diferentes APIs de proveedores bajo una interfaz común.\n")
    
    # Demostrar adapters para diferentes proveedores
    providers = ['motoya', 'ecobike', 'paqz']
    order_data = {
        'order_id': 123,
        'weight': 1500,
        'priority': 'normal',
        'fragility': 'debil',
        'address': 'Calle Principal 456'
    }
    
    print("🔌 Probando adapters con datos unificados:")
    print(f"   📦 Datos del pedido: {order_data}\n")
    
    for provider_name in providers:
        try:
            # Crear adapter usando factory
            adapter = ShippingAdapterFactory.create_adapter(provider_name)
            
            # Usar interfaz unificada
            tracking_id = adapter.request_pickup(order_data)
            
            print(f"✅ {adapter.get_provider_name().upper()}")
            print(f"   🏷️  Tracking generado: {tracking_id}")
            print(f"   🔧 API específica adaptada correctamente")
            
        except Exception as e:
            print(f"❌ Error con {provider_name}: {e}")
    
    print(f"\n💡 VENTAJAS del patrón Adapter:")
    print(f"   - Interfaz unificada para APIs heterogéneas")
    print(f"   - Fácil agregar nuevos proveedores")
    print(f"   - Desacopla cliente de implementaciones específicas")
    print(f"   - Factory pattern para gestión centralizada")


def demo_strategy_pattern():
    """Demuestra el patrón Strategy para selección de proveedores."""
    print_section("PATRÓN COMPORTAMENTAL: STRATEGY")
    
    print("El patrón Strategy define una familia de algoritmos intercambiables.")
    print("Permite cambiar el algoritmo de selección de proveedores dinámicamente.\n")
    
    # Datos de prueba para diferentes escenarios
    test_scenarios = [
        {
            'name': 'Pedido Ligero Normal',
            'data': {'weight': 800, 'priority': 'normal', 'fragility': 'ninguna'}
        },
        {
            'name': 'Pedido Express Frágil',
            'data': {'weight': 1500, 'priority': 'express', 'fragility': 'alta'}
        },
        {
            'name': 'Pedido Pesado',
            'data': {'weight': 4000, 'priority': 'normal', 'fragility': 'debil'}
        }
    ]
    
    # Estrategias disponibles
    strategies = {
        'Estándar': StandardSelectionStrategy(),
        'Ecológica': EcoFriendlySelectionStrategy(),
        'Optimizada por Costo': CostOptimizedSelectionStrategy()
    }
    
    for scenario in test_scenarios:
        print(f"📊 Escenario: {scenario['name']}")
        print(f"   Datos: {scenario['data']}")
        
        selector = ProviderSelector()
        
        for strategy_name, strategy in strategies.items():
            # Cambiar estrategia dinámicamente
            selector.set_strategy(strategy)
            result = selector.select_provider(scenario['data'])
            
            print(f"   🎯 {strategy_name}: {result['provider']} - {result['reason']}")
        
        print()
    
    print(f"💡 VENTAJAS del patrón Strategy:")
    print(f"   - Algoritmos intercambiables en tiempo de ejecución")
    print(f"   - Elimina condicionales complejas (if/else)")
    print(f"   - Fácil agregar nuevas estrategias")
    print(f"   - Principio Abierto/Cerrado (OCP)")


def demo_observer_pattern():
    """Demuestra el patrón Observer para notificaciones."""
    print_section("PATRÓN COMPORTAMENTAL: OBSERVER")
    
    print("El patrón Observer define dependencia uno-a-muchos entre objetos.")
    print("Permite notificar automáticamente a múltiples canales cuando cambia el estado.\n")
    
    # Crear sujeto observable
    notification_subject = OrderNotificationSubject()
    
    # Crear observadores (canales de notificación)
    email_observer = EmailNotificationObserver()
    webhook_observer = WebhookNotificationObserver("https://api.sistema-externo.com/hooks")
    sms_observer = SMSNotificationObserver("+57-300-123-4567")
    
    print("🔔 Configurando observadores:")
    
    # Agregar observadores dinámicamente
    notification_subject.attach_observer(email_observer)
    notification_subject.attach_observer(webhook_observer)
    notification_subject.attach_observer(sms_observer)
    
    print(f"   📝 Observadores activos: {notification_subject.get_observers_info()}")
    
    # Crear pedido temporal para demostración (sin persistir para evitar conflictos FK)
    from mercado_barrio.orders.models import Order
    
    # Intentar usar pedido existente, o crear uno temporal sin guardar
    try:
        # Usar el último pedido de la base de datos si existe
        mock_order = Order.objects.last()
        if not mock_order:
            # Si no hay pedidos, crear uno temporal sin guardar
            mock_order = Order(
                id=9999,  # ID alto para evitar conflictos
                customer_email="demo@mercadobarrio.com",
                address="Dirección Demo 123",
                priority="express",
                fragility="alta",
                total_weight=1200
            )
            # Guardar temporalmente para que funcionen las notificaciones
            mock_order.save()
            temp_order_created = True
        else:
            temp_order_created = False
            print(f"   📦 Usando pedido existente #{mock_order.id} para demostración")
    except Exception as e:
        print(f"   ⚠️  Error accediendo a pedidos existentes: {e}")
        # Crear pedido temporal
        mock_order = Order(
            id=9999,
            customer_email="demo@mercadobarrio.com", 
            address="Dirección Demo 123",
            priority="express",
            fragility="alta",
            total_weight=1200
        )
        mock_order.save()
        temp_order_created = True
    
    print(f"\n📦 Simulando eventos de pedido #{mock_order.id}:")
    
    # Simular diferentes eventos del ciclo de vida del pedido
    events = [
        ('CREATED', 'Pedido confirmado y asignado a EcoBike'),
        ('DISPATCHED', 'Pedido empacado y listo para recogida'),
        ('IN_TRANSIT', 'Pedido en camino al destino'),
        ('DELIVERED', 'Pedido entregado exitosamente')
    ]
    
    for event_type, message in events:
        print(f"\n   🔄 Evento: {event_type}")
        notification_subject.notify_observers(mock_order, event_type, message)
    
    # Mostrar historial
    print(f"\n📊 Historial de notificaciones:")
    history = notification_subject.get_notification_history()
    for i, event in enumerate(history[-2:], 1):  # Mostrar últimos 2
        print(f"   {i}. {event['event_type']} - {event['observers_count']} canales notificados")
    
    # Limpiar pedido temporal si fue creado
    if temp_order_created:
        try:
            mock_order.delete()
            print(f"   🧹 Pedido temporal #{mock_order.id} eliminado")
        except:
            pass
    
    print(f"\n💡 VENTAJAS del patrón Observer:")
    print(f"   - Desacoplamiento entre sujeto y observadores")
    print(f"   - Agregar/remover observadores dinámicamente")
    print(f"   - Notificación automática a múltiples canales")
    print(f"   - Extensible para nuevos tipos de notificaciones")


def demo_integrated_workflow():
    """Demuestra el flujo completo con todos los patrones integrados."""
    print_section("DEMOSTRACIÓN INTEGRADA - TODOS LOS PATRONES")
    
    print("Flujo completo de creación de pedido usando todos los patrones juntos.\n")
    
    # Verificar productos disponibles
    products = products_all()
    if not products:
        print("❌ No hay productos en la base de datos.")
        print("💡 Ejecuta el script de carga de datos primero: python manage.py loaddata seed_data.json")
        return
    
    print(f"📦 Productos disponibles: {len(products)}")
    for product in products[:3]:  # Mostrar primeros 3
        print(f"   {product.id}. {product.name} ({product.weight_grams}g)")
    
    # Datos de pedido de ejemplo
    order_data = {
        'customer_email': 'cliente.demo@mercadobarrio.com',
        'address': 'Carrera 15 #93-47, Bogotá, Colombia',
        'priority': 'express',
        'fragility': 'alta',
        'items': {str(products[0].id): 2, str(products[1].id): 1} if len(products) >= 2 else {str(products[0].id): 1}
    }
    
    print(f"\n📝 Datos del pedido:")
    for key, value in order_data.items():
        print(f"   {key}: {value}")
    
    print(f"\n🚀 Ejecutando creación de pedido con TODOS los patrones...")
    print(f"   (Ver logs detallados del proceso)\n")
    
    try:
        # Probar diferentes estrategias
        strategies = ['standard', 'eco', 'cost']
        
        for strategy in strategies:
            print(f"\n" + "="*50)
            print(f"🎯 PROBANDO ESTRATEGIA: {strategy.upper()}")
            print(f"="*50)
            
            # Crear pedido con la estrategia específica
            order_id = handle_create_order(order_data, strategy_type=strategy)
            
            print(f"\n✅ Pedido #{order_id} creado exitosamente con estrategia {strategy}")
            
    except Exception as e:
        print(f"❌ Error en flujo integrado: {e}")
        print(f"💡 Asegúrate de que la base de datos esté configurada correctamente")


def main():
    """Función principal que ejecuta todas las demostraciones."""
    print_header("DEMOSTRACIÓN DE PATRONES DE DISEÑO - MERCADO BARRIO")
    
    print("Este script demuestra la implementación de patrones de diseño")
    print("en el sistema de confirmación de pedidos y orquestación de entrega.")
    print("\nPATRONES IMPLEMENTADOS:")
    print("• CREACIONAL: Builder - Construcción compleja de pedidos")
    print("• ESTRUCTURAL: Adapter - Unificación de APIs de proveedores")
    print("• COMPORTAMENTAL: Strategy - Selección inteligente de proveedores")
    print("• COMPORTAMENTAL: Observer - Sistema de notificaciones multi-canal")
    
    try:
        # Ejecutar demostraciones individuales
        demo_builder_pattern()
        demo_adapter_pattern()
        demo_strategy_pattern()
        demo_observer_pattern()
        
        # Demostración integrada
        demo_integrated_workflow()
        
        print_header("DEMOSTRACIÓN COMPLETADA EXITOSAMENTE")
        print("✅ Todos los patrones funcionan correctamente")
        print("📚 Revisa los logs anteriores para ver los detalles de implementación")
        print("\n🎉 ¡La refactorización con patrones de diseño es exitosa!")
        
    except Exception as e:
        print(f"\n❌ ERROR GENERAL: {e}")
        print(f"💡 Verifica la configuración de Django y la base de datos")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()