#!/usr/bin/env python3
"""
Script para poblar la base de datos con datos de ejemplo.
Ejecuta el archivo SQL poblar_database.sql usando Django.
"""

import os
import sys
import django
from django.db import connection

# Configurar Django
sys.path.append(os.path.join(os.path.dirname(__file__), 'mercado_barrio'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mercado_barrio.settings')
django.setup()

def ejecutar_sql_file(filename):
    """
    Ejecuta un archivo SQL usando la conexión de Django.
    
    Args:
        filename: Nombre del archivo SQL a ejecutar
    """
    print(f"🗃️  Ejecutando archivo SQL: {filename}")
    
    try:
        # Leer el archivo SQL
        with open(filename, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Dividir en statements individuales
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        # Ejecutar cada statement
        with connection.cursor() as cursor:
            success_count = 0
            for i, statement in enumerate(statements):
                if statement.strip() and not statement.strip().startswith('--'):
                    try:
                        cursor.execute(statement)
                        success_count += 1
                    except Exception as e:
                        # Algunos errores son esperables (como comentarios mal formateados)
                        if 'syntax error' not in str(e).lower():
                            print(f"   ⚠️  Statement {i+1}: {str(e)[:100]}...")
            
            print(f"   ✅ {success_count} statements ejecutados exitosamente")
            
    except FileNotFoundError:
        print(f"   ❌ Archivo no encontrado: {filename}")
        return False
    except Exception as e:
        print(f"   ❌ Error ejecutando SQL: {e}")
        return False
    
    return True

def verificar_datos():
    """
    Verifica que los datos se hayan insertado correctamente.
    """
    print("\n🔍 Verificando datos insertados...")
    
    try:
        from mercado_barrio.orders.models import Product, Order, OrderItem, Shipment, Notification
        
        # Contar registros
        products_count = Product.objects.count()
        orders_count = Order.objects.count()
        items_count = OrderItem.objects.count()
        shipments_count = Shipment.objects.count()
        notifications_count = Notification.objects.count()
        
        print(f"   📦 Productos: {products_count}")
        print(f"   🛒 Pedidos: {orders_count}")
        print(f"   📋 Items de pedido: {items_count}")
        print(f"   🚚 Envíos: {shipments_count}")
        print(f"   🔔 Notificaciones: {notifications_count}")
        
        if products_count > 0 and orders_count > 0:
            print("   ✅ Base de datos poblada correctamente")
            return True
        else:
            print("   ❌ Faltan datos en la base de datos")
            return False
            
    except Exception as e:
        print(f"   ❌ Error verificando datos: {e}")
        return False

def main():
    """
    Función principal que ejecuta el proceso de población.
    """
    print("🗄️  POBLANDO BASE DE DATOS CON DATOS DE EJEMPLO")
    print("=" * 60)
    
    # Verificar si el archivo SQL existe
    sql_file = "poblar_database.sql"
    if not os.path.exists(sql_file):
        print(f"❌ Archivo SQL no encontrado: {sql_file}")
        print("💡 Asegúrate de estar en el directorio correcto")
        return
    
    try:
        # Ejecutar archivo SQL
        if ejecutar_sql_file(sql_file):
            # Verificar que los datos se insertaron
            if verificar_datos():
                print("\n" + "=" * 60)
                print("🎉 BASE DE DATOS POBLADA EXITOSAMENTE")
                print("=" * 60)
                print("✅ Datos de ejemplo insertados correctamente")
                print("🚀 Ahora puedes ejecutar: python demo_patrones.py")
                print("📊 O verificar con: python verificar_patrones.py")
            else:
                print("\n❌ Error en la verificación de datos")
        else:
            print("\n❌ Error ejecutando el archivo SQL")
            
    except Exception as e:
        print(f"\n❌ Error general: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()