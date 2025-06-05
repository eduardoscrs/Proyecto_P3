import random
from model.graph import Graph

class SimulationInitializer:
    def __init__(self):
        self.graph = Graph(directed=False)

    def generate_random_graph(self, n_nodes, m_edges):
        if n_nodes < 10 or n_nodes > 150 or m_edges < n_nodes - 1 or m_edges > 300:
            raise ValueError("Parámetros fuera de rango o grafo no conexo")
        
        # Crear nodos con roles
        nodes = []
        storage_count = int(n_nodes * 0.2)
        recharge_count = int(n_nodes * 0.2)
        client_count = n_nodes - storage_count - recharge_count
        
        for i in range(storage_count):
            nodes.append(self.graph.insert_vertex(f"S{i}", node_type="almacenamiento"))
        for i in range(recharge_count):
            nodes.append(self.graph.insert_vertex(f"R{i}", node_type="recarga"))
        for i in range(client_count):
            nodes.append(self.graph.insert_vertex(f"C{i}", node_type="cliente"))
        
        # Generar árbol base para garantizar conectividad
        random.shuffle(nodes)
        for i in range(1, len(nodes)):
            weight = random.randint(1, 20)  # Pesos aleatorios entre 1 y 20
            self.graph.insert_edge(nodes[i-1], nodes[i], weight)
            self.graph.insert_edge(nodes[i], nodes[i-1], weight)  # Grafo no dirigido
        
        # Agregar aristas adicionales hasta alcanzar m_edges
        remaining_edges = m_edges - (n_nodes - 1)
        while remaining_edges > 0:
            u, v = random.sample(nodes, 2)
            if not self.graph.get_edge(u, v):
                weight = random.randint(1, 20)
                self.graph.insert_edge(u, v, weight)
                self.graph.insert_edge(v, u, weight)
                remaining_edges -= 1
        
        return self.graph