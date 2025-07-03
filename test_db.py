from Proyect.data import SessionLocal, models

# Crear sesión de base de datos
db = SessionLocal()

# ✅ Crear cliente de prueba
cliente = models.Client(
    id="CL001",
    name="Juan Pérez",
    total_orders=3
)

# Guardar en la base
db.add(cliente)
db.commit()
db.refresh(cliente)

print("✅ Cliente insertado:")
print(f"ID: {cliente.id} | Nombre: {cliente.name} | Órdenes: {cliente.total_orders}")

# 🔍 Leer clientes existentes
print("\n📋 Lista de clientes en la base de datos:")
clientes = db.query(models.Client).all()
for c in clientes:
    print(f"- {c.id} | {c.name} | {c.total_orders} orden(es)")

# Cerrar sesión
db.close()
