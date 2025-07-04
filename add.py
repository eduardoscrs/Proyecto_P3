from sqlalchemy import create_engine, text

# Conectar a la base de datos
DATABASE_URL = "sqlite:///./app.db"  # Ajusta la URL de tu base de datos
engine = create_engine(DATABASE_URL)

# Ejecutar los comandos para cambiar el nombre de la columna
with engine.connect() as connection:
    try:
        # Crear una nueva tabla con la estructura corregida
        connection.execute("""
        CREATE TABLE new_orders AS
        SELECT id, origin AS origen, destino, status
        FROM orders
        """)

        # Eliminar la tabla vieja
        connection.execute("DROP TABLE orders")

        # Renombrar la nueva tabla a 'orders'
        connection.execute("ALTER TABLE new_orders RENAME TO orders")
        
        print("Columna 'origin' renombrada a 'origen' con éxito y tabla 'orders' actualizada.")
    except Exception as e:
        print(f"Error al ejecutar los comandos de renombrado de columna: {e}")
