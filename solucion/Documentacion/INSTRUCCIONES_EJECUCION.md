# 🚀 Instrucciones de Ejecución - Patrones de Diseño MercadoBarrio

## 📋 Problema Identificado

El error que experimentaste se debe a que la demostración intentaba crear notificaciones para un pedido simulado (ID #999) que no existía en la base de datos, violando la restricción de clave foránea.

## ✅ Solución Implementada

He creado **múltiples opciones** para poblar la base de datos con datos de ejemplo:

1. **Comando Django** (Recomendado)
2. **Script Python independiente**
3. **Archivo SQL directo**

---

## 🎯 Opción 1: Comando Django (RECOMENDADO)

### Paso 1: Poblar la Base de Datos
```bash
cd solucion/
python manage.py poblar_datos
```

### Opciones del comando:
```bash
# Poblar con datos nuevos
python manage.py poblar_datos

# Limpiar datos existentes y poblar
python manage.py poblar_datos --limpiar
```

### Paso 2: Ejecutar Demostración
```bash
python demo_patrones.py
```

---

## 🎯 Opción 2: Script Python Independiente

### Paso 1: Poblar la Base de Datos
```bash
cd solucion/
python poblar_db.py
```

### Paso 2: Ejecutar Demostración
```bash
python demo_patrones.py
```

---

## 🎯 Opción 3: SQL Directo (Para usuarios avanzados)

### Paso 1: Ejecutar SQL manualmente
```bash
# Conectar a PostgreSQL y ejecutar:
psql -U tu_usuario -d tu_database -f poblar_database.sql
```

### Paso 2: Ejecutar Demostración
```bash
python demo_patrones.py
```

---

## 📦 Datos que se Crean

### ✅ **30 Productos**
- **Ligeros**: Arroz, aceite, sal, etc. (300-1000g)
- **Medianos**: Detergentes, champús, etc. (1000-2500g)
- **Pesados**: Bultos, cajas, etc. (3000-8000g)
- **Frágiles**: Copas, platos, electrónicos, etc.
- **Frágiles pesados**: Vajillas, espejos, etc.

### ✅ **10 Pedidos de Ejemplo**
- **Normales ligeros**: Para probar MotoYA
- **Express frágiles**: Para probar EcoBike
- **Pesados**: Para probar PaqueteríaZ
- **Mixtos**: Para probar diferentes estrategias

### ✅ **Items de Pedido**
- Distribución realista de productos por pedido
- Pesos calculados correctamente

### ✅ **10 Envíos**
- Diferentes proveedores: MotoYA, EcoBike, PaqueteríaZ
- Estados variados: CONFIRMADO, DESPACHADO, EN_RUTA, ENTREGADO
- Tracking IDs generados automáticamente

### ✅ **Notificaciones Multi-canal**
- Email, Webhook, SMS
- Para diferentes eventos del ciclo de vida

---

## 🧪 Verificaciones Disponibles

### Verificación Rápida
```bash
python verificar_patrones.py
```

### Verificación con Datos
```bash
python demo_patrones.py
```

### Verificación Manual Django
```bash
python manage.py shell
>>> from mercado_barrio.orders.models import *
>>> print(f"Productos: {Product.objects.count()}")
>>> print(f"Pedidos: {Order.objects.count()}")
```

---

## 🎉 Salida Esperada

Después de poblar la base de datos, `demo_patrones.py` debería mostrar:

```
================================================================================
  DEMOSTRACIÓN DE PATRONES DE DISEÑO - MERCADO BARRIO
================================================================================

🔹 PATRÓN CREACIONAL: BUILDER
✅ Builder configurado exitosamente:
   📧 Cliente: cliente@ejemplo.com
   📦 Código paquete: PKG-A1B2C3D4E5F6
   🏷️  Etiqueta: FRÁGIL - MANEJAR CON EXTREMO CUIDADO

🔹 PATRÓN ESTRUCTURAL: ADAPTER
🔌 Probando adapters con datos unificados:
✅ MOTOYA - Tracking generado: MYA-ABC123
✅ ECOBIKE - Tracking generado: EBK-DEF456
✅ PAQZ - Tracking generado: PAQ-GHI789

🔹 PATRÓN COMPORTAMENTAL: STRATEGY
📊 Escenario: Pedido Ligero Normal
   🎯 Estándar: motoya - Proveedor motoya seleccionado para pedido de 800g
   🎯 Ecológica: ecobike - Proveedor ecobike seleccionado para pedido de 800g

🔹 PATRÓN COMPORTAMENTAL: OBSERVER
🔔 Configurando observadores:
➕ Observador agregado: Notificador Email
➕ Observador agregado: Notificador Webhook
➕ Observador agregado: Notificador SMS

📦 Simulando eventos de pedido #1:
🔔 Notificando evento CREATED para pedido #1
📧 EMAIL enviado a cliente1@mercadobarrio.com: ¡Pedido #1 confirmado!
🔗 WEBHOOK enviado a https://api.sistema-externo.com/hooks: {...}
📱 SMS enviado a +57-300-123-4567: Pedido #1 confirmado

🔹 DEMOSTRACIÓN INTEGRADA - TODOS LOS PATRONES
🚀 Ejecutando creación de pedido con TODOS los patrones...

🔨 Aplicando patrón BUILDER para construcción del pedido...
   ✅ Pedido #11 construido exitosamente

📋 Aplicando patrón STRATEGY (standard) para selección de proveedor...
   ✅ Proveedor seleccionado: motoya

🔌 Aplicando patrón ADAPTER para integración con motoya...
   ✅ Integración exitosa con motoya

🔔 Aplicando patrón OBSERVER para notificaciones...
   ✅ Notificaciones enviadas a 3 canales

🎉 PEDIDO CREADO EXITOSAMENTE CON PATRONES DE DISEÑO
```

---

## ❌ Solución de Problemas

### Error de Clave Foránea
- **Causa**: Pedido simulado no existe en BD
- **Solución**: Ejecutar cualquiera de los scripts de población

### No hay productos
- **Causa**: Base de datos vacía
- **Solución**: `python manage.py poblar_datos`

### Error de Django
- **Causa**: Django no configurado
- **Solución**: Verificar settings y migraciones
```bash
python manage.py migrate
python manage.py poblar_datos
```

### Error de conexión BD
- **Causa**: PostgreSQL no ejecutándose
- **Solución**: Iniciar PostgreSQL y verificar configuración

---

## 📚 Archivos Creados

- ✅ **`poblar_database.sql`**: Script SQL completo
- ✅ **`poblar_db.py`**: Script Python independiente  
- ✅ **`poblar_datos.py`**: Comando Django management
- ✅ **`demo_patrones.py`**: Demostración actualizada (sin errores FK)
- ✅ **`INSTRUCCIONES_EJECUCION.md`**: Este archivo

---

## 🎯 Próximos Pasos

1. **Ejecutar**: `python manage.py poblar_datos`
2. **Verificar**: `python verificar_patrones.py`
3. **Demostrar**: `python demo_patrones.py`
4. **Revisar**: Logs detallados de cada patrón
5. **Explorar**: Documentación en `DOCUMENTACION_PATRONES.md`

¡Ahora la demostración debería funcionar perfectamente sin errores de clave foránea! 🎉