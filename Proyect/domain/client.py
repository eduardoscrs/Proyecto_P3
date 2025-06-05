class Client:
    def __init__(self, id_cliente, nombre, ubi_nodo):
        self.id = id_cliente
        self.nombre = nombre
        self.ubi_nodo = ubi_nodo  # nodo en el grafo (ej. "F")
        self.total_ordenes = 0

    def incremento_ordenes(self):
        self.total_ordenes += 1

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "ubicación": self.ubi_nodo,
            "total_ordenes": self.total_ordenes
        }


cliente1= Client(123, "juan", "F")
print(cliente1.to_dict())

cliente1.incremento_ordenes()
print(cliente1.to_dict())