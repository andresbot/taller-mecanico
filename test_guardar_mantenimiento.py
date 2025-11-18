"""
Script de prueba para verificar si se guardan los mantenimientos correctamente
"""
from controllers.mantenimiento_controller import MantenimientoController
from controllers.vehiculo_controller import VehiculoController
from services.db_service import DatabaseService

# Obtener el primer vehículo disponible
vehiculo_controller = VehiculoController()
vehiculos = vehiculo_controller.get_all()

if not vehiculos:
    print("ERROR: No hay vehículos en la base de datos")
    exit(1)

vehiculo = vehiculos[0]
print(f"\n=== PRUEBA DE GUARDADO DE MANTENIMIENTO ===")
print(f"Vehículo seleccionado: {vehiculo.placa} - {vehiculo.marca} {vehiculo.modelo}")
print(f"ID del vehículo: {vehiculo.id}")

# Crear un mantenimiento de prueba
controller = MantenimientoController()

print("\n--- Intentando crear un Cambio de Aceite ---")
try:
    mantenimiento_id = controller.create_cambio_aceite(
        vehiculo_id=vehiculo.id,
        kilometraje=50000,
        mecanico="ANDRES BOTERO",
        observaciones="Prueba de guardado automático",
        filtro_aceite="FRAM PH-123",
        filtro_aire="K&N 33-2345",
        tipo_aceite="5W30 Sintético"
    )
    print(f"✓ Mantenimiento creado con ID: {mantenimiento_id}")
except Exception as e:
    print(f"✗ ERROR al crear mantenimiento: {e}")
    import traceback
    traceback.print_exc()

# Verificar que se guardó en la base de datos
print("\n--- Verificando en la base de datos ---")
db = DatabaseService()

# Contar mantenimientos
result = db.execute_query("SELECT COUNT(*) as total FROM mantenimientos")
print(f"Total de mantenimientos en DB: {result[0]['total']}")

# Obtener el último mantenimiento
result = db.execute_query("""
    SELECT m.*, ca.filtro_aceite, ca.filtro_aire, ca.tipo_aceite 
    FROM mantenimientos m
    LEFT JOIN cambio_aceite ca ON ca.mantenimiento_id = m.ID
    ORDER BY m.ID DESC 
    LIMIT 1
""")
if result:
    print(f"\nÚltimo mantenimiento registrado:")
    for key, value in result[0].items():
        print(f"  {key}: {value}")
else:
    print("✗ No se encontró el mantenimiento en la base de datos")

# Verificar con el controlador
print("\n--- Verificando con el controlador ---")
historial = controller.get_by_vehiculo(vehiculo.id)
print(f"Mantenimientos del vehículo {vehiculo.placa}: {len(historial)}")
for m in historial:
    print(f"  - {m.fecha_mantenimiento} | {m.tipo_mantenimiento} | KM: {m.kilometraje} | {m.mecanico}")

print("\n=== FIN DE LA PRUEBA ===\n")
