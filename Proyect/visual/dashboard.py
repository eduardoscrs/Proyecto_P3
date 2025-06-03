import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from model.graph import Graph
from sim.init_simulation import SimulationInitializer
from tda.avl import Node, insert, to_networkx, pre_order
from tda.hash_map import Map
import random

st.set_page_config(layout="wide")

# Estado de la sesión para almacenar el grafo y datos 
if "graph" not in st.session_state:
    st.session_state.graph = None
if "orders" not in st.session_state:
    st.session_state.orders = Map()
if "clients" not in st.session_state:
    st.session_state.clients = Map()
if "routes_avl" not in st.session_state:
    st.session_state.routes_avl = None

# Pestaña 1: Run Simulation
def run_simulation():
    st.header("Run Simulation")
    n_nodes = st.slider("Número de nodos", 10, 150, 15)
    m_edges = st.slider("Número de aristas", n_nodes - 1, 300, 20)
    n_orders = st.slider("Número de órdenes", 10, 300, 10)
    st.write(f"Nodos: {n_nodes} (Clientes: {int(n_nodes * 0.6)}, Almacenamiento: {int(n_nodes * 0.2)}, Recarga: {int(n_nodes * 0.2)})")
    
    if st.button("Start Simulation"):
        initializer = SimulationInitializer()
        st.session_state.graph = initializer.generate_random_graph(n_nodes, m_edges)
        st.session_state.routes_avl = None
        st.session_state.orders = Map()
        st.session_state.clients = Map()
        for v in st.session_state.graph.vertices():
            if st.session_state.graph.get_node_type(v) == "cliente":
                st.session_state.clients.put(v.element(), {"id": v.element(), "name": f"Client {v.element()}", "type": "cliente", "total_orders": 0})
        for i in range(n_orders):
            client = random.choice([v for v in st.session_state.graph.vertices() if st.session_state.graph.get_node_type(v) == "cliente"])
            storage = random.choice([v for v in st.session_state.graph.vertices() if st.session_state.graph.get_node_type(v) == "almacenamiento"])
            path, cost = st.session_state.graph.find_path_with_battery(storage, client)
            if path:
                route_key = tuple(v.element() for v in path)
                st.session_state.routes_avl = insert(st.session_state.routes_avl, route_key)
                order_id = f"O{i}"
                st.session_state.orders.put(order_id, {
                    "id": order_id, "client_id": client.element(), "origin": storage.element(),
                    "destination": client.element(), "status": "pending", "cost": cost
                })
                client_data = st.session_state.clients.get(client.element())
                client_data["total_orders"] += 1
                st.session_state.clients.put(client.element(), client_data)
        st.success("Simulación iniciada")

# Pestaña 2: Explore Network
def explore_network():
    st.header("Explore Network")
    if st.session_state.graph:
        G = nx.Graph()
        for v in st.session_state.graph.vertices():
            node_type = st.session_state.graph.get_node_type(v)
            color = {"almacenamiento": "blue", "recarga": "green", "cliente": "red"}.get(node_type, "gray")
            G.add_node(v.element(), color=color)
        for e in st.session_state.graph.edges():
            u, v = e.endpoints()
            G.add_edge(u.element(), v.element(), weight=e.element())
        
        fig, ax = plt.subplots()
        pos = nx.spring_layout(G)
        node_colors = [G.nodes[n]["color"] for n in G.nodes]
        nx.draw(G, pos, with_labels=True, node_color=node_colors, ax=ax)
        st.pyplot(fig)
        
        nodes = [v.element() for v in st.session_state.graph.vertices()]
        origin = st.selectbox("Nodo origen", nodes)
        destination = st.selectbox("Nodo destino", nodes)
        if st.button("Calculate Route"):
            origin_vertex = next(v for v in st.session_state.graph.vertices() if v.element() == origin)
            dest_vertex = next(v for v in st.session_state.graph.vertices() if v.element() == destination)
            path, cost = st.session_state.graph.find_path_with_battery(origin_vertex, dest_vertex)
            if path:
                path_str = " -> ".join(v.element() for v in path)
                st.write(f"Path: {path_str} | Cost: {cost}")
                st.session_state.routes_avl = insert(st.session_state.routes_avl, tuple(v.element() for v in path))
                if st.button("Complete Delivery and Create Order"):
                    order_id = f"O{len(st.session_state.orders)}"
                    st.session_state.orders.put(order_id, {
                        "id": order_id, "client_id": destination, "origin": origin,
                        "destination": destination, "status": "completed", "cost": cost
                    })
                    client_data = st.session_state.clients.get(destination)
                    client_data["total_orders"] += 1
                    st.session_state.clients.put(destination, client_data)
            else:
                st.error("No se encontró ruta válida")
    else:
        st.warning("Inicie una simulación primero")

# Pestaña 3: Clients & Orders
def clients_orders():
    st.header("Clients & Orders")
    if st.session_state.graph:
        st.subheader("Clientes")
        st.json([st.session_state.clients.get(k) for k in st.session_state.clients._table if k])
        st.subheader("Órdenes")
        st.json([st.session_state.orders.get(k) for k in st.session_state.orders._table if k])
    else:
        st.warning("Inicie una simulación primero")

# Pestaña 4: Route Analytics
def route_analytics():
    st.header("Route Analytics")
    if st.session_state.routes_avl:
        st.subheader("Rutas más frecuentes")
        pre_order(st.session_state.routes_avl)
        G = to_networkx(st.session_state.routes_avl)
        fig, ax = plt.subplots()
        pos = nx.spring_layout(G)
        labels = nx.get_node_attributes(G, "label")
        nx.draw(G, pos, with_labels=True, labels=labels, ax=ax)
        st.pyplot(fig)
    else:
        st.warning("No hay rutas registradas")

# Pestaña 5: General Statistics
def general_statistics():
    st.header("General Statistics")
    if st.session_state.graph:
        client_visits = {k: v["total_orders"] for k, v in [(k, st.session_state.clients.get(k)) for k in st.session_state.clients._table if k]}
        storage_visits = {v.element(): sum(o["cost"] for o in [st.session_state.orders.get(k) for k in st.session_state.orders._table if k] if o["origin"] == v.element())
                         for v in st.session_state.graph.vertices() if st.session_state.graph.get_node_type(v) == "almacenamiento"}
        recharge_visits = {v.element(): sum(1 for o in [st.session_state.orders.get(k) for k in st.session_state.orders._table if k] if v.element() in o["destination"])
                          for v in st.session_state.graph.vertices() if st.session_state.graph.get_node_type(v) == "recarga"}
        
        fig, ax = plt.subplots()
        ax.bar(client_visits.keys(), client_visits.values(), label="Clientes")
        ax.bar(storage_visits.keys(), storage_visits.values(), label="Almacenamiento")
        ax.bar(recharge_visits.keys(), recharge_visits.values(), label="Recarga")
        ax.legend()
        st.pyplot(fig)
        
        node_counts = {
            "Clientes": sum(1 for v in st.session_state.graph.vertices() if st.session_state.graph.get_node_type(v) == "cliente"),
            "Almacenamiento": sum(1 for v in st.session_state.graph.vertices() if st.session_state.graph.get_node_type(v) == "almacenamiento"),
            "Recarga": sum(1 for v in st.session_state.graph.vertices() if st.session_state.graph.get_node_type(v) == "recarga")
        }
        fig, ax = plt.subplots()
        ax.pie(node_counts.values(), labels=node_counts.keys(), autopct="%1.1f%%")
        st.pyplot(fig)
    else:
        st.warning("Inicie una simulación primero")

# Configuración de pestañas
tabs = st.tabs(["Run Simulation", "Explore Network", "Clients & Orders", "Route Analytics", "General Statistics"])
with tabs[0]:
    run_simulation()
with tabs[1]:
    explore_network()
with tabs[2]:
    clients_orders()
with tabs[3]:
    route_analytics()
with tabs[4]:
    general_statistics()