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
    nx_graph = nx.DiGraph()
    graph = Graph(directed=True)

    # Asignar roles
    num_storage = int(num_nodes * 0.2)
    num_recharge = int(num_nodes * 0.2)
    num_client = num_nodes - num_storage - num_recharge

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

    storage_nodes = node_names[:num_storage]
    recharge_nodes = node_names[num_storage:num_storage + num_recharge]
    client_nodes = node_names[num_storage + num_recharge:]

    for name in storage_nodes:
        graph.insert_vertex(name, node_type="almacenamiento")
        nx_graph.add_node(name, tipo="almacenamiento")
    for name in recharge_nodes:
        graph.insert_vertex(name, node_type="recarga")
        nx_graph.add_node(name, tipo="recarga")
    for name in client_nodes:
        graph.insert_vertex(name, node_type="cliente")
        nx_graph.add_node(name, tipo="cliente")

    # Conectar nodos de forma fuerte (ida y vuelta)
    added_edges = set()
    connected = set()
    available = list(node_names)
    random.shuffle(available)

    first = available.pop()
    connected.add(first)

    # Conectar como un árbol (n - 1 aristas)
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

    # AVL de pedidos y rutas
    pedido_avl = AVLTree()
    route_avl = AVLTree()
    orders = []

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

        # Buscar ruta válida con bfs (considerando autonomía)
        try:
            path = bfs(graph, origin, destination, max_cost=50)
            if path:
                route = Route(path, cost=len(path))
                route_avl.insert(route)
        except Exception:
            pass  # rutas no válidas se ignoran

    # Clientes en hash map
    clientes = Map()
    for name in client_nodes:
        client = Client(client_id=name, name=f"Client{name}")
        for order in orders:
            if order.client_id == name:
                client.add_order()
        clientes.put(name, client)

    return {
        "nx_graph": nx_graph,
        "graph": graph,
        "orders": orders,
        "storage_nodes": storage_nodes,
        "client_nodes": client_nodes,
        "recharge_nodes": recharge_nodes,
        "clientes": clientes,
        "pedido_avl_root": pedido_avl.root,
        "route_avl": route_avl
    }
