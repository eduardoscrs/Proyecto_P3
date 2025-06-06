from Proyect.model.graph import Graph
from Proyect.tda.hash_map import Map
from Proyect.tda import avl
from Proyect.model.graph_utils import bfs


def run_simulation(origin, destination, priority):
    graph = Graph(directed=True)

    # Insertar nodos
    a = graph.insert_vertex("A", node_type="almacenamiento")
    b = graph.insert_vertex("B", node_type="cliente")
    c = graph.insert_vertex("C", node_type="recarga")
    d = graph.insert_vertex("D", node_type="cliente")

    # Insertar aristas
    graph.insert_edge(a, b, 30)
    graph.insert_edge(b, c, 10)
    graph.insert_edge(a, c, 20)
    graph.insert_edge(c, d, 25)
    graph.insert_edge(b, d, 40)

    # AVL de pedidos (simulado)
    pedido_avl_root = None
    for pedido_id in [105, 103, 110]:
        pedido_avl_root = avl.insert(pedido_avl_root, pedido_id)

    # Clientes en Hash Map
    clientes = Map()
    clientes.put("B", {"nombre": "Cliente B", "pedidos": [105]})
    clientes.put("D", {"nombre": "Cliente D", "pedidos": [103, 110]})

    # Obtener vértices de origen y destino
    v_origen = next((v for v in graph.vertices() if v.element() == origin), None)
    v_destino = next((v for v in graph.vertices() if v.element() == destination), None)

    if not v_origen or not v_destino:
        return {"error": "Origen o destino no válido"}

    # Buscar ruta
    path, cost = graph.find_path_with_battery(v_origen, v_destino, max_battery=50)

    resultado = {
        "origen": origin,
        "destino": destination,
        "prioridad": priority,
        "ruta": [v.element() for v in path] if path else None,
        "costo": cost if path else None,
        "pedidos": clientes.get(destination)["pedidos"] if clientes.get(destination) else []
    }

    return resultado
