import streamlit as st
st.set_page_config(page_title="Drone Logistics Simulator", layout="wide")  # ¡Debe ir primero!
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import requests
import folium
from matplotlib.patches import Patch
from Proyect.sim.simulation import run_simulation_dynamic
from Proyect.visual.avl_visualizer import draw_avl_tree
from Proyect.tda.avl import AVLTree
from Proyect.model.graph_utils import dijkstra, reconstruct_path
from streamlit_folium import st_folium

def start_simulation(num_nodes, num_edges, num_orders):
    url = "http://localhost:8002/run_simulation/"
    response = requests.post(url, json={
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "num_orders": num_orders
    })
    return response.json()

if st.button("Start Simulation"):
    result = start_simulation(num_nodes=15, num_edges=20, num_orders=10)
    st.write(result)

# ---------- UTILS ----------
def plot_node_distribution(num_storage, num_recharge, num_clientes):
    labels = ['Storage', 'Recharge', 'Client']
    values = [num_storage, num_recharge, num_clientes]
    colors = ['#f39c12', '#3498db', '#2ecc71']

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    ax.set_title("Node Role Distribution")
    return fig

def draw_network(nx_graph, path=None):
    tipo_color = {
        "almacenamiento": "#f39c12",
        "recarga": "#3498db",
        "cliente": "#2ecc71"
    }
    num_nodes = nx_graph.number_of_nodes()
    try:
        if num_nodes <= 30:
            pos = nx.spring_layout(nx_graph, seed=42)
        elif num_nodes <= 100:
            pos = nx.kamada_kawai_layout(nx_graph)
        else:
            pos = nx.shell_layout(nx_graph)
    except:
        pos = nx.spring_layout(nx_graph, seed=42)

    node_colors = [tipo_color.get(nx_graph.nodes[n].get("tipo", ""), "#95a5a6") for n in nx_graph.nodes]
    edge_colors = ["red" if path and (u, v) in zip(path, path[1:]) else "gray" for u, v in nx_graph.edges]
    node_size = 800 if num_nodes <= 30 else 400 if num_nodes <= 100 else 200
    font_size = 10 if num_nodes <= 30 else 8 if num_nodes <= 100 else 6

    plt.figure(figsize=(12, 9))
    nx.draw(nx_graph, pos, with_labels=True,
            node_color=node_colors,
            edge_color=edge_colors,
            node_size=node_size,
            width=2.5,
            font_size=font_size,
            font_weight='bold')
    if num_nodes <= 50:
        edge_labels = nx.get_edge_attributes(nx_graph, 'weight')
        nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels=edge_labels, font_size=font_size)

    legend_elements = [
        Patch(facecolor=tipo_color["almacenamiento"], label="Storage"),
        Patch(facecolor=tipo_color["recarga"], label="Recharge"),
        Patch(facecolor=tipo_color["cliente"], label="Client"),
    ]
    plt.legend(handles=legend_elements, loc="lower left", fontsize=font_size + 1)
    st.pyplot(plt.gcf())

# --- NUEVO: Battery-aware Dijkstra ---
def battery_aware_dijkstra(graph, origin_v, destination_v, recharge_nodes, autonomy=50):
    """
    Dijkstra que fuerza recarga si la distancia entre nodos supera la autonomía.
    Retorna (path, total_cost) o (None, None) si no hay ruta.
    """
    path = []
    total_cost = 0
    current = origin_v
    while True:
        distances, prev = dijkstra(graph, current)
        # Buscar si se puede llegar directo
        if distances.get(destination_v, float('inf')) <= autonomy:
            sub_path = reconstruct_path(prev, current, destination_v)
            if not sub_path:
                return None, None
            path += sub_path[1:] if path else sub_path
            total_cost += distances[destination_v]
            break
        # Buscar estación de recarga alcanzable más cercana al destino
        min_cost = float('inf')
        next_recharge = None
        best_subpath = None
        for r in recharge_nodes:
            v_r = graph.get_vertex(r)
            if v_r == current:
                continue
            if distances.get(v_r, float('inf')) <= autonomy:
                # Desde esta estación, ¿puedo llegar al destino?
                d2, _ = dijkstra(graph, v_r)
                if d2.get(destination_v, float('inf')) < min_cost:
                    min_cost = d2[destination_v]
                    next_recharge = v_r
                    best_subpath = reconstruct_path(prev, current, v_r)
        if not next_recharge or not best_subpath:
            return None, None
        path += best_subpath[1:] if path else best_subpath
        total_cost += distances[next_recharge]
        current = next_recharge
    return path, total_cost

# ---------- MAIN APP ----------
def main():
    st.title("🚁 Drone Logistics Simulator - Correos Chile")

    tabs = st.tabs([
        "🔁 Run Simulation",
        "🌍 Explore Network",
        "🌐 Clients & Orders",
        "📋 Route Analytics",
        "📈 Statistics"
    ])

    # 1. Run Simulation
    with tabs[0]:
        st.subheader("Initialize Simulation")
        num_nodos = st.slider("Number of Nodes", 10, 150, 15)
        num_aristas = st.slider("Number of Edges", 10, 300, 20)
        num_ordenes = st.slider("Number of Orders", 1, 500, 10)

        num_storage = int(num_nodos * 0.2)
        num_recharge = int(num_nodos * 0.2)
        num_clientes = num_nodos - num_storage - num_recharge

        st.markdown(f"""
        **Node Role Proportions:**
        - 📦 Storage Nodes: {num_storage} (20%)
        - 🔋 Recharge Nodes: {num_recharge} (20%)
        - 👤 Client Nodes: {num_clientes} (60%)
        """)

        if st.button("🟢 Start Simulation"):
            result = run_simulation_dynamic(num_nodos, num_aristas, num_ordenes)
            avl_tree = AVLTree()
            try:
                for order in result["orders"]:
                    path = nx.shortest_path(result["nx_graph"], order.origin, order.destination, weight="weight")
                    route_str = " → ".join(path)
                    avl_tree.insert(route_str)
            except:
                pass
            result["route_avl"] = avl_tree
            st.session_state["last_simulation"] = result
            st.session_state.pop("last_path", None)
            st.session_state.pop("last_cost", None)
            st.success("Simulation completed!")

    # 2. Explore Network
    with tabs[1]:
        st.header("🌍 Network Visualization (Folium)")
        if "last_simulation" not in st.session_state:
            st.warning("Initialize a simulation first.")
        else:
            sim_data = st.session_state["last_simulation"]
            nx_graph = sim_data["nx_graph"]
            graph = sim_data["graph"]
            storage_nodes = sim_data["storage_nodes"]
            client_nodes = sim_data["client_nodes"]
            recharge_nodes = sim_data["recharge_nodes"]
            node_options_storage = storage_nodes
            node_options_client = client_nodes

            # Dummy geolocations for demo (replace with real if available)
            import random
            random.seed(42)
            # Centered near Lima, Peru
            node_coords = {n: (random.uniform(-12.06, -12.03), random.uniform(-77.04, -77.01)) for n in nx_graph.nodes}

            col1, col2 = st.columns([0.35, 0.65])
            with col1:
                st.subheader("Select Route")
                origen = st.selectbox("Origin Node (Storage)", node_options_storage)
                destino = st.selectbox("Destination Node (Client)", node_options_client)
                algoritmo = st.radio("Algorithm", ["Dijkstra", "Floyd-Warshall"], index=0)
                calcular = st.button("✈️ Calculate Route")
                complete_delivery = st.button("✅ Complete Delivery and Create Order")
                show_mst = st.button("🌲 Show MST (Kruskal)")
            with col2:
                st.subheader("Geographical Map (Folium)")
                # Cambiar centro del mapa a Lima, Perú
                m = folium.Map(location=[-12.04318, -77.02824], zoom_start=13)
                for n, (lat, lon) in node_coords.items():
                    tipo = nx_graph.nodes[n].get("tipo", "")
                    color = {"almacenamiento": "orange", "recarga": "blue", "cliente": "green"}.get(tipo, "gray")
                    folium.CircleMarker([lat, lon], radius=7, color=color, fill=True, fill_opacity=0.8, popup=f"{n} ({tipo})").add_to(m)
                for u, v, d in nx_graph.edges(data=True):
                    latlngs = [node_coords[u], node_coords[v]]
                    folium.PolyLine(latlngs, color="#888", weight=2, opacity=0.5, tooltip=f"{u}→{v} ({d.get('weight', '')})").add_to(m)
                route_path = None
                route_cost = None
                # --- NUEVO: Cálculo y visualización separados ---
                if calcular:
                    # Validar solo almacenamiento→cliente
                    if origen not in storage_nodes or destino not in client_nodes:
                        st.error("Solo se permiten rutas de Almacenamiento a Cliente.")
                    else:
                        origin_v = graph.get_vertex(origen)
                        destination_v = graph.get_vertex(destino)
                        if algoritmo == "Dijkstra":
                            route_path, total_cost = battery_aware_dijkstra(graph, origin_v, destination_v, recharge_nodes, autonomy=50)
                        else:
                            from Proyect.model.graph_utils import floyd_warshall_path
                            route_path, total_cost = floyd_warshall_path(graph, origin_v, destination_v, recharge_nodes, autonomy=50)
                        if route_path:
                            route_path = [v.element() if hasattr(v, 'element') else v for v in route_path]
                            st.session_state["last_path"] = route_path
                            st.session_state["last_cost"] = total_cost
                            st.success(f"Ruta calculada: {' → '.join(route_path)} | Distancia: {total_cost}")
                        else:
                            st.session_state["last_path"] = None
                            st.session_state["last_cost"] = None
                            st.error("❌ No hay ruta factible con batería.")
                route_path = st.session_state.get("last_path", None)
                route_cost = st.session_state.get("last_cost", None)
                # Dibujar ruta calculada
                if route_path:
                    for i in range(len(route_path)-1):
                        u, v_ = route_path[i], route_path[i+1]
                        folium.PolyLine([node_coords[u], node_coords[v_]], color="red", weight=5, opacity=0.9).add_to(m)
                # Mostrar MST si se solicita
                if show_mst:
                    from Proyect.model.graph_utils import kruskal_mst
                    mst_edges = kruskal_mst(graph)
                    for u, v in mst_edges:
                        folium.PolyLine([node_coords[u], node_coords[v]], color="#00ff00", weight=4, opacity=0.7, dash_array='10,10').add_to(m)
                st_folium(m, width=700, height=500)
                # Resumen de vuelo
                if route_path:
                    st.info(f"Resumen de vuelo: Ruta {' → '.join(route_path)}, Distancia: {route_cost}")

    # 3. Clients & Orders
    with tabs[2]:
        st.header("🌐 Clients and Orders")
        if "last_simulation" in st.session_state:
            clientes = st.session_state["last_simulation"]["clientes"]
            orders_map = st.session_state["last_simulation"]["orders_map"]
            clientes_data = [v.to_dict() for _, v in clientes.items()]
            st.subheader("Clients (from hash map)")
            st.json(clientes_data)

            orders = st.session_state["last_simulation"]["orders"]
            orders_data = [o.to_dict() for o in orders]
            st.subheader("Orders (from list)")
            st.json(orders_data)

            # --- NUEVO: Buscar cliente y orden por ID usando el hash map ---
            st.markdown("---")
            st.subheader("🔎 Buscar Cliente u Orden por ID (usando hash map)")
            col1, col2 = st.columns(2)
            with col1:
                client_id = st.text_input("Client ID para buscar", "")
                if client_id:
                    client_obj = clientes.get(client_id)
                    if client_obj:
                        st.success(f"Cliente encontrado: {client_obj.to_dict()}")
                    else:
                        st.warning("Cliente no encontrado en el hash map.")
            with col2:
                order_id = st.text_input("Order ID para buscar", "")
                if order_id:
                    order_obj = orders_map.get(order_id)
                    if order_obj:
                        st.success(f"Orden encontrada: {order_obj.to_dict()}")
                    else:
                        st.warning("Orden no encontrada en el hash map.")
    # 4. Route Analytics
    with tabs[3]:
        st.header("📋 Route Analytics")
        if "last_simulation" not in st.session_state or "route_avl" not in st.session_state["last_simulation"]:
            st.info("No routes recorded yet.")
        else:
            avl_tree = st.session_state["last_simulation"]["route_avl"]
            st.subheader("🌿 Rutas Frecuentes (AVL In-Order)")
            for i, (ruta, freq) in enumerate(avl_tree.get_top_routes(10), 1):
                st.markdown(f"{i}. `{ruta}` → Freq: **{freq}**")
            st.subheader("🌳 AVL Visual (Rutas)")
            draw_avl_tree(avl_tree, title="AVL Tree - Frequent Routes")


    # 5. Statistics
    with tabs[4]:
        st.header("📈 General Statistics")
        if "last_simulation" in st.session_state:
            sim = st.session_state["last_simulation"]

            # Crear columnas para los gráficos de barras
            col1, col2, col3 = st.columns(3)

            # Bar Chart - Most Visited Clients
            with col1:
                st.subheader("Most Visited Clients")
                most_visited_clients = {k: v for k, v in sim["clientes"].items() if hasattr(v, 'total_orders')}
                most_visited_clients = sorted(most_visited_clients.items(), key=lambda x: x[1].total_orders, reverse=True)
                client_labels = [client[0] for client in most_visited_clients]
                client_values = [client[1].total_orders for client in most_visited_clients]
                client_data = pd.DataFrame({'Client': client_labels, 'Visits': client_values})
                st.bar_chart(client_data.set_index('Client'))

            # Bar Chart - Most Visited Recharge Stations
            with col2:
                st.subheader("Most Visited Recharge Stations")
                most_visited_recharge = {node: sim["nx_graph"].degree(node) for node in sim["recharge_nodes"]}
                recharge_data = pd.DataFrame(list(most_visited_recharge.items()), columns=['Station', 'Visits'])
                st.bar_chart(recharge_data.set_index('Station'))

            # Bar Chart - Most Visited Storage Nodes
            with col3:
                st.subheader("Most Visited Storage Nodes")
                most_visited_storage = {node: sim["nx_graph"].degree(node) for node in sim["storage_nodes"]}
                storage_data = pd.DataFrame(list(most_visited_storage.items()), columns=['Storage Node', 'Visits'])
                st.bar_chart(storage_data.set_index('Storage Node'))

            # Node Distribution Pie Chart (after bar charts)
            st.subheader("Node Role Distribution")
            fig, ax = plt.subplots(figsize=(5, 5))  # Reducido tamaño del gráfico de pastel
            labels = ['Storage', 'Recharge', 'Client']
            values = [len(sim["storage_nodes"]), len(sim["recharge_nodes"]), len(sim["client_nodes"])]
            colors = ['#f39c12', '#3498db', '#2ecc71']
            ax.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            ax.set_title("Node Role Distribution")
            st.pyplot(fig)

        else:
            st.warning("You need to run a simulation first.")
# NOTE: If you want to use Vertex objects as dict keys, ensure Vertex implements __hash__ and __eq__ based on .element().
