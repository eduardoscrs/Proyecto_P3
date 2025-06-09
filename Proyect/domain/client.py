class Client:
    def __init__(self, client_id, name, client_type="normal"):
        self.client_id = client_id
        self.name = name
        self.type = client_type
        self.total_orders = 0

    def to_dict(self):
        return {
            "client_id": self.client_id,
            "name": self.name,
            "type": self.type,
            "total_orders": self.total_orders
        }

    def add_order(self):
        self.total_orders += 1
