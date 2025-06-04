from .vertex import Vertex
from .edge import Edge
from collections import deque

class Graph:
    def __init__(self, directed=False):
        self._outgoing = {}
        self._incoming = {} if directed else self._outgoing
        self._directed = directed
        self._node_types = {}  # Diccionario para almacenar tipos de nodos (almacenamiento, recarga, cliente)

    def is_directed(self):
        return self._directed

    def insert_vertex(self, element, node_type=None):
        v = Vertex(element)
        self._outgoing[v] = {}
        if self._directed:
            self._incoming[v] = {}
        self._node_types[v] = node_type  # Asignar tipo de nodo
        return v

    def insert_edge(self, u, v, element):
        e = Edge(u, v, element)
        self._outgoing[u][v] = e
        self._incoming[v][u] = e
        return e

    def remove_edge(self, u, v):
        if u in self._outgoing and v in self._outgoing[u]:
            del self._outgoing[u][v]
            del self._incoming[v][u]

    def remove_vertex(self, v):
        for u in list(self._outgoing.get(v, {})):
            self.remove_edge(v, u)
        for u in list(self._incoming.get(v, {})):
            self.remove_edge(u, v)
        self._outgoing.pop(v, None)
        if self._directed:
            self._incoming.pop(v, None)
        self._node_types.pop(v, None)

    def get_edge(self, u, v):
        return self._outgoing.get(u, {}).get(v)

    def vertices(self):
        return self._outgoing.keys()

    def edges(self):
        seen = set()
        for map in self._outgoing.values():
            seen.update(map.values())
        return seen

    def neighbors(self, v):
        return self._outgoing[v].keys()

    def degree(self, v, outgoing=True):
        adj = self._outgoing if outgoing else self._incoming
        return len(adj[v])

    def incident_edges(self, v, outgoing=True):
        adj = self._outgoing if outgoing else self._incoming
        return adj[v].values()

    def get_node_type(self, v):
        return self._node_types.get(v, None)

    def find_path_with_battery(self, start, end, max_battery=50):
        """Encuentra la ruta más corta desde start a end respetando la autonomía del dron."""
        queue = deque([(start, [start], 0)])  # (nodo_actual, camino, costo_acumulado)
        visited = set()
        while queue:
            current, path, cost = queue.popleft()
            if current == end:
                return path, cost
            if (current, cost) in visited:
                continue
            visited.add((current, cost))
            for neighbor in self.neighbors(current):
                edge = self.get_edge(current, neighbor)
                edge_cost = edge.element() if edge else 0
                new_cost = cost + edge_cost
                # Si el vecino es una estación de recarga, reiniciar batería
                if self.get_node_type(neighbor) == "recarga":
                    new_cost = edge_cost
                if new_cost <= max_battery:
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path, new_cost))
        return None, 0  # No se encontró ruta válida