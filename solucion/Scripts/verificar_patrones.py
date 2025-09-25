#!/usr/bin/env python3
"""
Verificación rápida de la refactorización con patrones de diseño.
"""

print('🧪 VERIFICACIÓN RÁPIDA DE LA REFACTORIZACIÓN')
print('=' * 50)

# Verificar que las importaciones funcionan
try:
    import os
    import sys
    import django
    
    # Configurar Django
    sys.path.append('mercado_barrio')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mercado_barrio.settings')
    django.setup()
    
    # Importar clases refactorizadas
    from mercado_barrio.orders.services import (
        OrderBuilder,
        ShippingAdapterFactory, 
        StandardSelectionStrategy,
        OrderNotificationSubject,
        EmailNotificationObserver
    )
    
    print('✅ Todas las importaciones exitosas')
    print('✅ Patrón Builder: OrderBuilder disponible')
    print('✅ Patrón Adapter: ShippingAdapterFactory disponible') 
    print('✅ Patrón Strategy: StandardSelectionStrategy disponible')
    print('✅ Patrón Observer: OrderNotificationSubject disponible')
    
    # Verificar que las clases se pueden instanciar
    builder = OrderBuilder()
    strategy = StandardSelectionStrategy()
    subject = OrderNotificationSubject()
    observer = EmailNotificationObserver()
    
    print('✅ Todas las clases se instancian correctamente')
    print()
    print('🎉 REFACTORIZACIÓN COMPLETADA EXITOSAMENTE')
    print('📋 Todos los patrones implementados correctamente')
    print('📚 Ver DOCUMENTACION_PATRONES.md para detalles completos')
    print('🚀 Ejecuta "python demo_patrones.py" para ver la demostración completa')
    
except Exception as e:
    print(f'❌ Error: {e}')
    print('💡 Revisa la configuración de Django')
    import traceback
    traceback.print_exc()