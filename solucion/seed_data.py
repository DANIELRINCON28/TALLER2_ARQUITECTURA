import os
import django
import sys

# Configurar Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mercado_barrio.settings')
django.setup()

from mercado_barrio.orders.models import Product

# Limpiar productos existentes
Product.objects.all().delete()

# Crear productos
products = [
    Product(sku='VEL-AROMA', name='Vela aromática', weight_grams=300, fragile=True),
    Product(sku='TE-VERDE', name='Té verde 250g', weight_grams=250, fragile=False),
    Product(sku='TAZA-CE', name='Taza cerámica', weight_grams=400, fragile=True),
    Product(sku='CUCH-META', name='Cuchillo metálico', weight_grams=150, fragile=False),
    Product(sku='LIB-AG', name='Agenda pequeña', weight_grams=200, fragile=False),
]

Product.objects.bulk_create(products)

print(f'✅ {len(products)} productos cargados exitosamente')
for product in Product.objects.all():
    fragile_text = "Frágil" if product.fragile else "No frágil"
    print(f"  - {product.sku}: {product.name} ({product.weight_grams}g, {fragile_text})")