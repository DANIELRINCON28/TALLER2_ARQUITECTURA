"""
Script para cargar datos iniciales en la base de datos.
Equivalente directo de seed.sql del proyecto PHP original.
Este script debe ejecutarse después de las migraciones.

Uso:
python manage.py shell
exec(open('load_initial_data.py').read())
"""
from orders.models import Product

def load_products():
    """
    Carga los productos iniciales equivalentes a seed.sql.
    Traducción directa de:
    INSERT INTO products (sku,name,weight_grams,fragile) VALUES
    ('VEL-AROMA','Vela aromática', 300, 1),
    ('TE-VERDE','Té verde 250g', 250, 0),
    ('TAZA-CE','Taza cerámica', 400, 1),
    ('CUCH-META','Cuchillo metálico', 150, 0),
    ('LIB-AG','Agenda pequeña', 200, 0)
    """
    print("Cargando productos iniciales (equivalente a seed.sql)...")
    
    # Limpiar productos existentes si existen
    Product.objects.all().delete()
    
    # Crear productos - traducción directa de seed.sql
    products = [
        Product(sku='VEL-AROMA', name='Vela aromática', weight_grams=300, fragile=True),
        Product(sku='TE-VERDE', name='Té verde 250g', weight_grams=250, fragile=False),
        Product(sku='TAZA-CE', name='Taza cerámica', weight_grams=400, fragile=True),
        Product(sku='CUCH-META', name='Cuchillo metálico', weight_grams=150, fragile=False),
        Product(sku='LIB-AG', name='Agenda pequeña', weight_grams=200, fragile=False),
    ]
    
    # Equivalente a ON DUPLICATE KEY UPDATE en MySQL
    Product.objects.bulk_create(products, ignore_conflicts=True)
    
    print(f"✅ {len(products)} productos cargados exitosamente")
    print("Los productos cargados son:")
    for product in Product.objects.all():
        fragile_text = "Frágil" if product.fragile else "No frágil"
        print(f"  - {product.sku}: {product.name} ({product.weight_grams}g, {fragile_text})")

if __name__ == "__main__":
    # Este script debe ejecutarse dentro del contexto de Django
    print("⚠️  Este script debe ejecutarse con: python manage.py shell")
    print("   Luego ejecutar: exec(open('load_initial_data.py').read())")
else:
    # Se está ejecutando dentro del shell de Django
    load_products()