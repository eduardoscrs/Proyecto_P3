# init_db.py

from Proyect.data.database import Base, engine
from Proyect.data import models  # Importar modelos para registrar las tablas

def reset_db():
    """
    Elimina todas las tablas y las vuelve a crear (reset de la base de datos).
    """
    print("⚠️ Borrando todas las tablas...")
    Base.metadata.drop_all(bind=engine)  # Elimina todas las tablas
    print("✅ Tablas eliminadas.")
    
    print("📦 Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)  # Vuelve a crear las tablas
    print("✅ Tablas creadas exitosamente.")

def init():
    reset_db()

if __name__ == "__main__":
    init()
