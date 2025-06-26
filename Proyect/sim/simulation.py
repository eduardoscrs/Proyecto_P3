import networkx as nx
import random
from Proyect.model.graph import Graph
from Proyect.tda.hash_map import Map
from Proyect.tda.avl import AVLTree
from Proyect.model.graph_utils import bfs
from Proyect.domain.client import Client
from Proyect.domain.order import Order
from Proyect.domain.route import Route

def run_simulation_dynamic(num_nodes, num_edges, num_orders):
    # Crear grafos
    nx_graph = nx.DiGraph()  # Grafo de NetworkX para visualización
    graph = Graph(directed=True)  # Grafo personalizado para simulación

    # Asignar roles de nodos
    num_storage = int(num_nodes * 0.2)  # Nodos de almacenamiento
    num_recharge = int(num_nodes * 0.2)  # Nodos de recarga
    num_client = num_nodes - num_storage - num_recharge  # Nodos de clientes

    # Generar nombres de nodos
    def generate_node_names(n):
        from string import ascii_uppercase
        names = []
        i = 0
        while len(names) < n:
            if i < 26:
                names.append(ascii_uppercase[i])
            else:
                names.append(ascii_uppercase[i // 26 - 1] + ascii_uppercase[i % 26])
            i += 1
        return names

    node_names = generate_node_names(num_nodes)
    random.shuffle(node_names)

    # Asignar nombres a nodos de diferentes tipos
    storage_nodes = node_names[:num_storage]
    recharge_nodes = node_names[num_storage:num_storage + num_recharge]
    client_nodes = node_names[num_storage + num_recharge:]

    # Insertar nodos en el grafo
    for name in storage_nodes:
        graph.insert_vertex(name, node_type="almacenamiento")
        nx_graph.add_node(name, tipo="almacenamiento")
    for name in recharge_nodes:
        graph.insert_vertex(name, node_type="recarga")
        nx_graph.add_node(name, tipo="recarga")
    for name in client_nodes:
        graph.insert_vertex(name, node_type="cliente")
        nx_graph.add_node(name, tipo="cliente")

    # Conectar nodos con aristas bidireccionales
    added_edges = set()
    connected = set()
    available = list(node_names)
    random.shuffle(available)

    first = available.pop()
    connected.add(first)

    # Conectar como un árbol (n-1 aristas)
    while available:
        u = random.choice(list(connected))
        v = available.pop()
        weight = random.randint(5, 30)
        u_vertex = graph.get_vertex(u)
        v_vertex = graph.get_vertex(v)
        graph.insert_edge(u_vertex, v_vertex, weight)
        graph.insert_edge(v_vertex, u_vertex, weight)  # bidireccional
        nx_graph.add_edge(u, v, weight=weight)
        nx_graph.add_edge(v, u, weight=weight)
        added_edges.add((u, v))
        added_edges.add((v, u))
        connected.add(v)

    # Asegurar que haya suficientes aristas
    while len(added_edges) < num_edges:
        u, v = random.sample(node_names, 2)
        if (u, v) not in added_edges and u != v:
            weight = random.randint(5, 30)
            u_vertex = graph.get_vertex(u)
            v_vertex = graph.get_vertex(v)
            graph.insert_edge(u_vertex, v_vertex, weight)
            graph.insert_edge(v_vertex, u_vertex, weight)  # bidireccional
            nx_graph.add_edge(u, v, weight=weight)
            nx_graph.add_edge(v, u, weight=weight)
            added_edges.add((u, v))
            added_edges.add((v, u))

    # Crear árboles AVL para registrar pedidos y rutas
    pedido_avl = AVLTree()
    route_avl = AVLTree()
    orders = []

    # Generar pedidos
    for i in range(num_orders):
        origin = random.choice(storage_nodes)
        destination = random.choice(client_nodes)
        priority = random.randint(1, 3)
        order_id = f"{100+i}"
        client_id = destination
        client_name = f"Client{client_id}"

        order = Order(
            order_id=order_id,
            client=client_name,
            client_id=client_id,
            origin=origin,
            destination=destination,
            priority=priority
        )

        pedido_avl.insert(int(order_id))
        orders.append(order)

        # Buscar ruta válida usando BFS (considerando autonomía)
        try:
            path = bfs(graph, origin, destination, max_cost=50)
            if path:
                route = Route(path, cost=len(path))
                route_avl.insert(route)
        except Exception:
            pass  # Ignorar rutas no válidas

    # Crear clientes en el hash map
    clientes = Map()
    for name in client_nodes:
        client = Client(client_id=name, name=f"Client{name}")
        for order in orders:
            if order.client_id == name:
                client.add_order()
        clientes.put(name, client)

    # Crear órdenes en el hash map
    orders_map = Map()
    for order in orders:
        orders_map.put(order.order_id, order)

    return {
        "nx_graph": nx_graph,  # Grafo de NetworkX
        "graph": graph,  # Grafo personalizado
        "orders": orders,
        "orders_map": orders_map,
        "storage_nodes": storage_nodes,
        "client_nodes": client_nodes,
        "recharge_nodes": recharge_nodes,
        "clientes": clientes,
        "pedido_avl_root": pedido_avl.root,
        "route_avl": route_avl
    }

# Función para obtener la ruta más corta usando Dijkstra
def dijkstra_shortest_path(graph, source, target):
    try:
        path = nx.shortest_path(graph, source=source, target=target, weight='weight')
        return path
    except nx.NetworkXNoPath:
        return {"error": "No path exists between these nodes"}
