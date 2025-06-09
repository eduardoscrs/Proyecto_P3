class Route:
    def __init__(self, path, cost):
        self.path = path  # lista de nodos
        self.cost = cost

    def __str__(self):
        return " → ".join(self.path)
