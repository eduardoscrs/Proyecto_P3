import streamlit as st
import networkx as nx
import random
import matplotlib.pyplot as plt
import string  


def generar_nombres_letras(n):
    letras = []
    abecedario = list(string.ascii_uppercase)
    for i in range(n):
        if i < 26:
            letras.append(abecedario[i])
        else:
            letras.append(abecedario[i // 26 - 1] + abecedario[i % 26])
    return letras

# BFS
def bfs_con_bateria(grafo, inicio, fin, bateria_max=50):
    from collections import deque

    cola = deque()
    cola.append((inicio, [inicio], 0))  # nodo actual, camino, batería usada
    visitados = set()

    while cola:
        actual, camino, bateria = cola.popleft()

        if actual == fin:
            return camino, bateria

        visitados.add((actual, bateria))

        for vecino in grafo.neighbors(actual):
            peso = grafo[actual][vecino]['weight']
            nueva_bateria = bateria + peso

            if (vecino, nueva_bateria) in visitados:
                continue

            
            if nueva_bateria > bateria_max:
                if grafo.nodes[vecino]['tipo'] == "🔋":
                    nueva_bateria = 0  
                else:
                    continue

            cola.append((vecino, camino + [vecino], nueva_bateria))

    return None, None


# CONFIGURACIÓN GENERAL
st.set_page_config(page_title="Simulación Drones", layout="wide")
st.markdown("## 🚁 Drone Logistics Simulator - Correos Chile")

st.markdown("""
**Node Role Proportions:**
- 📦 **Storage Nodes**: 20%
- 🔋 **Recharge Nodes**: 20%
- 🧔 **Client Nodes**: 60%
""")

st.divider()

# PESTAÑAS
tab1, tab2, _, _, _ = st.tabs([
    "🔄 Run Simulation",
    "🌍 Explore Network",
    "🌐 Clients & Orders",
    "📋 Route Analytics",
    "📈 Statistics"
])

# -------------------- PESTAÑA 1 --------------------
with tab1:
    st.subheader("⚙️ Initialize Simulation")

    n_nodes = st.slider("Number of Nodes", 10, 150, 30)
    m_edges = st.slider("Number of Edges", max(n_nodes - 1, 10), 300, 43)
    n_orders = st.slider("Number of Orders", 1, 500, 10)

    storage = int(n_nodes * 0.2)
    charging = int(n_nodes * 0.2)
    clients = n_nodes - storage - charging

    st.caption(f"Derived Client Nodes: {clients} (60% of {n_nodes})")

    if st.button("🟢 Start Simulation"):
        st.success("✅ Simulation started!")

        G = nx.Graph()
        nombres_nodos = generar_nombres_letras(n_nodes)

        for i, nombre in enumerate(nombres_nodos):
            if i < storage:
                G.add_node(nombre, tipo="📦")
            elif i < storage + charging:
                G.add_node(nombre, tipo="🔋")
            else:
                G.add_node(nombre, tipo="👤")

        connected = list(nombres_nodos)
        random.shuffle(connected)
        for i in range(n_nodes - 1):
            G.add_edge(connected[i], connected[i + 1], weight=random.randint(1, 20))

        while G.number_of_edges() < m_edges:
            a, b = random.sample(nombres_nodos, 2)
            if not G.has_edge(a, b):
                G.add_edge(a, b, weight=random.randint(1, 20))

        st.session_state["grafo"] = G
        st.session_state["simulacion_activa"] = True

# -------------------- PESTAÑA 2 --------------------
with tab2:
    st.header("🌍 Network visualization")

    if "grafo" not in st.session_state:
        st.warning("Primero debes iniciar la simulación desde la pestaña 1.")
    else:
        G = st.session_state["grafo"]
        pos = nx.spring_layout(G)
        colores = {"📦": "blue", "🔋": "green", "👤": "orange"}
        node_colors = [colores[G.nodes[n]["tipo"]] for n in G.nodes]
        leyenda = {"📦": "Almacenamiento", "🔋": "Recarga", "👤": "Cliente"}

        # Controles a la derecha
        col1, col2 = st.columns([3, 1])

        with col2:
            origen = st.selectbox("Origin Node", list(G.nodes))
            destino = st.selectbox("Destination Node", list(G.nodes))

            calcular = st.button("🛩️ Calculate Route")

        # Dibujar grafo (único)
        with col1:
            fig, ax = plt.subplots(figsize=(8, 6))

            # Si se calculó ruta, dibujarla en rojo
            if calcular:
                try:
                    camino, costo = bfs_con_bateria(G, origen, destino)

                    if camino is None:
                        st.error("No hay ruta posible con la batería disponible.")
                    else:
                        st.success(f"Ruta: {' → '.join(map(str, camino))} | Costo: {costo}")
                        edges = list(zip(camino, camino[1:]))
                        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='red', width=2, ax=ax)

                        if st.button("✅ Complete Delivery and Create Order"):
                            st.info("Orden creada correctamente (simulado)")
                except:
                    st.error("Error al calcular la ruta.")

            # Siempre dibujar nodos y leyenda (con o sin ruta)
            nx.draw(G, pos, with_labels=True, node_color=node_colors, ax=ax)
            for emoji, desc in leyenda.items():
                ax.plot([], [], color=colores[emoji], label=f"{emoji} {desc}", marker='o', linestyle='')
            ax.legend()
            st.pyplot(fig)
