from Proyect.model.graph import Graph
from Proyect.tda.hash_map import Map
from Proyect.tda import avl

def run_simulation():
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

    # Pedidos en AVL
    pedido_avl_root = None
    for pedido_id in [105, 103, 110]:
        pedido_avl_root = avl.insert(pedido_avl_root, pedido_id)

    # Clientes en Hash Map
    clientes = Map()
    clientes.put("B", {"nombre": "Cliente B", "pedidos": [105]})
    clientes.put("D", {"nombre": "Cliente D", "pedidos": [103, 110]})

    # Resultados de rutas
    resultados = []

    for cliente_id in ["B", "D"]:
        cliente_vertex = None
        for v in graph.vertices():
            if v.element() == cliente_id:
                cliente_vertex = v
                break

        if cliente_vertex:
            path, cost = graph.find_path_with_battery(a, cliente_vertex, max_battery=50)
            if path:
                resultados.append({
                    "cliente": cliente_id,
                    "ruta": [v.element() for v in path],
                    "costo": cost,
                    "pedidos": clientes.get(cliente_id)["pedidos"]
                })
            else:
                resultados.append({
                    "cliente": cliente_id,
                    "ruta": None,
                    "costo": None,
                    "pedidos": clientes.get(cliente_id)["pedidos"]
                })

    return resultados
