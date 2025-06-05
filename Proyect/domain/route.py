class Route:
    def __init__(self, path, cost):
        self.path = path  # lista de nodos: ["A", "B", "C"]
        self.cost = cost

    def get_key(self):
        return " → ".join(self.path)

    def to_dict(self):
        return {
            "path": self.path,
            "cost": self.cost
        }


ruta = Route(["A", "D", "F"], 18)

print(
    f"path: {ruta.path}\n"
    f"cost: {ruta.cost}"
)  # {'path': ['A', 'D', 'F'], 'cost': 18}
