from Proyect.data import Base, engine
from Proyect.data import models  # Importar modelos para registrar las tablas

print("Creando tablas en la base de datos...")
Base.metadata.create_all(bind=engine)
print(" Tablas creadas exitosamente.")
