import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from Proyect.sim.simulation import run_simulation_dynamic

def draw_network(nx_graph, path=None):
    import matplotlib.pyplot as plt
    import networkx as nx

    tipo_color = {
        "almacenamiento": "#f39c12",
        "recarga": "#3498db",
        "cliente": "#2ecc71"
    }

    num_nodes = nx_graph.number_of_nodes()

    # Layout adaptativo
    if num_nodes <= 30:
        pos = nx.spring_layout(nx_graph, seed=42)
    elif num_nodes <= 100:
        pos = nx.kamada_kawai_layout(nx_graph)
    else:
        pos = nx.shell_layout(nx_graph)  # Más ordenado en nodos grandes

    node_colors = [tipo_color.get(nx_graph.nodes[n].get("tipo", ""), "#95a5a6") for n in nx_graph.nodes]
    edge_colors = ["red" if path and (u, v) in zip(path, path[1:]) else "gray" for u, v in nx_graph.edges]

    # Tamaño dinámico
    node_size = 800 if num_nodes <= 30 else 400 if num_nodes <= 100 else 200
    font_size = 10 if num_nodes <= 30 else 8 if num_nodes <= 100 else 6

    plt.figure(figsize=(12, 8 if num_nodes <= 100 else 10))
    nx.draw(nx_graph, pos, with_labels=True,
            node_color=node_colors,
            edge_color=edge_colors,
            node_size=node_size,
            width=1.8,
            font_size=font_size,
            font_weight='bold')

    # Etiquetas de peso solo para grafos pequeños
    if num_nodes <= 50:
        edge_labels = nx.get_edge_attributes(nx_graph, 'weight')
        nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels=edge_labels, font_size=font_size)

    st.pyplot(plt.gcf())


def main():
    st.set_page_config(page_title="Simulación de Rutas", layout="wide")
    st.title("📦 Simulador de Rutas de Entrega")

    st.markdown("Bienvenido al sistema de simulación logística de Correos Chile.")

    tabs = st.tabs(["🔁 Simulación", "🗺️ Visualización", "📋 Clientes y órdenes", "📊 Estadísticas"])

# 1. Simulación
    with tabs[0]:
        st.markdown("### Proporciones de roles de nodo (calculadas dinámicamente):")
        
        col1, col2 = st.columns([0.7, 0.3])

        with col1:
            num_nodos = st.slider("🔢 Número de nodos", 10, 150, 15)
            num_aristas = st.slider("🔗 Número de aristas", 10, 300, 20)
            num_ordenes = st.slider("📦 Número de órdenes", 1, 500, 10)

            # Cálculo dinámico de proporciones
            num_storage = int(num_nodos * 0.2)
            num_recharge = int(num_nodos * 0.2)
            num_clientes = num_nodos - num_storage - num_recharge

            st.markdown(f"""
            **🧮 Distribución estimada:**
            - 🟫 Almacenamiento: {num_storage} ({round((num_storage/num_nodos)*100)}%)
            - 🟦 Recarga: {num_recharge} ({round((num_recharge/num_nodos)*100)}%)
            - 🟩 Cliente: {num_clientes} ({round((num_clientes/num_nodos)*100)}%)
            """)

        with col2:
            st.subheader(" ")
            if st.button("🟢 Iniciar simulación"):
                result = run_simulation_dynamic(num_nodos, num_aristas, num_ordenes)
                st.session_state["last_simulation"] = result
                st.success("✅ Simulación completada")

    # 2. Visualización
    with tabs[1]:
        st.header("🗺️ Visualización de Red de Entregas")
        if "last_simulation" not in st.session_state:
            st.warning("⚠️ Debes ejecutar una simulación primero.")
        else:
            nx_graph = st.session_state["last_simulation"]["nx_graph"]
            node_options = list(nx_graph.nodes)

            col_mapa, col_controles = st.columns([0.65, 0.35])
            with col_controles:
                st.subheader("📍 Calcular Ruta")
                origen = st.selectbox("🟢 Nodo de Origen", node_options)
                destino = st.selectbox("🔴 Nodo de Destino", node_options, index=1)
                calcular = st.button("🚀 Calcular Ruta")

            with col_mapa:
                st.subheader("🌐 Grafo de la Red de Entrega")
                path = None
                if origen != destino and calcular:
                    try:
                        path = nx.shortest_path(nx_graph, origen, destino, weight="weight")
                        cost = nx.shortest_path_length(nx_graph, origen, destino, weight="weight")
                        st.success(f"Ruta: {' ➡️ '.join(path)} (Costo total: {cost})")
                    except nx.NetworkXNoPath:
                        st.error("❌ No existe una ruta entre esos nodos.")
                draw_network(nx_graph, path)

    # 3. Clientes y Órdenes
    with tabs[2]:
        st.header("📋 Información de Clientes y Órdenes")
        if "last_simulation" in st.session_state:
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("👤 Clientes")
                clientes = st.session_state["last_simulation"]["clientes"]
                data = [{"Cliente": k, "Pedidos": v["pedidos"]} for k, v in clientes.items()]
                st.dataframe(data, use_container_width=True)

            with col2:
                st.subheader("📦 Órdenes")
                orders = st.session_state["last_simulation"]["orders"]
                st.dataframe(orders, use_container_width=True)
        else:
            st.warning("⚠️ Debes ejecutar una simulación primero.")

    # 5. Estadísticas
    with tabs[3]:
        st.header("📊 Estadísticas del Sistema")
        st.info("Frecuencia de uso de nodos, rutas frecuentes, y análisis de entregas.")
        st.markdown("📈 En desarrollo...")

if __name__ == "__main__":
    main()
