from datetime import datetime

class Order:
    def __init__(self, order_id, client, client_id, origin, destination, priority=0):
        self.order_id = order_id
        self.client = client
        self.client_id = client_id
        self.origin = origin
        self.destination = destination
        self.status = "pending"
        self.priority = priority
        self.created_at = datetime.now()
        self.delivered_at = None
        self.route_cost = None

    def complete(self, route_cost):
        self.status = "delivered"
        self.delivered_at = datetime.now()
        self.route_cost = route_cost
        
    def to_dict(self):
        return {
            "order_id": self.order_id,
            "client": self.client,
            "client_id": self.client_id,
            "origin": self.origin,
            "destination": self.destination,
            "status": self.status,
            "priority": self.priority,
            "created_at": self.created_at.isoformat(),
            "delivered_at": self.delivered_at.isoformat() if self.delivered_at else None,
            "route_cost": self.route_cost
        }
