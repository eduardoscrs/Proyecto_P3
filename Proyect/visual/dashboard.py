import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from Proyect.sim.simulation import run_simulation_dynamic
from Proyect.visual.avl_visualizer import draw_avl_tree
from Proyect.tda.avl import AVLTree

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

# ---------- MAIN APP ----------
def main():
    st.set_page_config(page_title="Drone Logistics Simulator", layout="wide")
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
        st.header("🌍 Network Visualization")
        if "last_simulation" not in st.session_state:
            st.warning("Initialize a simulation first.")
        else:
            nx_graph = st.session_state["last_simulation"]["nx_graph"]
            node_options = list(nx_graph.nodes)
            col1, col2 = st.columns([0.35, 0.65])
            with col1:
                st.subheader("📌 Calculate Route")
                origen = st.selectbox("Origin Node", node_options)
                destino = st.selectbox("Destination Node", node_options, index=1)
                calcular = st.button("🚀 Calculate Route")

            with col2:
                st.subheader("🌐 Graph View")
                if calcular and origen != destino:
                    try:
                        if not nx.has_path(nx_graph, origen, destino):
                            st.error("❌ No existe una ruta posible.")
                        else:
                            path = nx.shortest_path(nx_graph, origen, destino, weight="weight")
                            cost = nx.shortest_path_length(nx_graph, origen, destino, weight="weight")
                            st.session_state["last_path"] = path
                            st.session_state["last_cost"] = cost
                            st.success(f"Path: {' → '.join(path)} | Cost: {cost}")
                    except Exception as e:
                        st.error(f"Error: {e}")

                draw_network(nx_graph, st.session_state.get("last_path"))

    # 3. Clients & Orders
    with tabs[2]:
        st.header("🌐 Clients and Orders")
        if "last_simulation" in st.session_state:
            clientes = st.session_state["last_simulation"]["clientes"]
            clientes_data = [v.to_dict() for _, v in clientes.items()]
            st.subheader("Clients")
            st.json(clientes_data)

            orders = st.session_state["last_simulation"]["orders"]
            orders_data = [o.to_dict() for o in orders]
            st.subheader("Orders")
            st.json(orders_data)

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
            fig = plot_node_distribution(
                len(sim["storage_nodes"]),
                len(sim["recharge_nodes"]),
                len(sim["client_nodes"])
            )
            st.pyplot(fig)
        else:
            st.warning("You need to run a simulation first.")

if __name__ == "__main__":
    main()
