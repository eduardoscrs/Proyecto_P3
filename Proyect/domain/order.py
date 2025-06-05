import datetime

class Order:
    def __init__(self, order_id, client_id, origin, destination, path, cost, priority=1):
        self.id = order_id
        self.client_id = client_id
        self.origin = origin
        self.destination = destination
        self.path = path
        self.cost = cost
        self.status = "delivered"
        self.created_at = datetime.datetime.now()
        self.delivered_at = datetime.datetime.now()
        self.priority = priority

    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "origin": self.origin,
            "destination": self.destination,
            "path": self.path,
            "cost": self.cost,
            "status": self.status,
            "created_at": str(self.created_at),
            "delivered_at": str(self.delivered_at),
            "priority": self.priority
        }


orden = Order(1, 101, "A", "F", ["A", "C", "F"], 150.0, 2)

print(
    f"ID: {orden.id}\n"
    f"Cliente: {orden.client_id}\n"
    f"Origen: {orden.origin}\n"
    f"Destino: {orden.destination}\n"
    f"Ruta: {orden.path}\n"
    f"Costo: {orden.cost}\n"
    f"Estado: {orden.status}\n"
    f"Creado: {orden.created_at}\n"
    f"Entregado: {orden.delivered_at}\n"
    f"Prioridad: {orden.priority}\n"
)

