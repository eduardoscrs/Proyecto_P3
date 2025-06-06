import streamlit as st
from Proyect.sim.simulation import run_simulation
from Proyect.model.graph import Graph
from Proyect.domain.client import Client
from Proyect.domain.order import Order
import random

# Nodos simulados (reemplaza esto por el grafo real más adelante)
NODES = ["A", "B", "C", "D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","V"]

# Inicializar sesión
if "ordenes" not in st.session_state:
    st.session_state["ordenes"] = []

if "clientes" not in st.session_state:
    st.session_state["clientes"] = {}

# ------------------------- APP -------------------------
def main():
    st.set_page_config(page_title="Simulación de Rutas", layout="wide")
    st.title("📦 Simulador de Rutas de Entrega")

    st.markdown("""
    Bienvenido al sistema de simulación logística. Aquí puedes crear simulaciones, visualizar rutas, consultar clientes, órdenes, y revisar estadísticas del sistema.
    """)

    tabs = st.tabs([
        "🔁 Simulación",
        "🗺️ Visualización",
        "👤 Clientes",
        "📦 Órdenes",
        "📊 Estadísticas"
    ])

    # ----------------------- 1. Simulación -----------------------
    



    with tabs[0]:
        st.header("🔁 Crear Simulación")

        # 1. Sliders para configuración
        n_nodes = st.slider("Cantidad de nodos", 10, 150, 15)
        n_edges = st.slider("Cantidad de aristas", n_nodes - 1, 300, min(20, n_nodes + 5))
        n_orders = st.slider("Cantidad de órdenes", 1, 500, 10)

        if st.button("🚀 Ejecutar Simulación"):
            # Crear grafo desde cero sin SimulationInitializer
            graph = Graph(directed=False)

            # Asignación de roles a nodos
            storage_count = int(n_nodes * 0.2)
            recharge_count = int(n_nodes * 0.2)
            client_count = n_nodes - storage_count - recharge_count

            nodes = []
            for i in range(storage_count):
                nodes.append(graph.insert_vertex(f"S{i}", node_type="almacenamiento"))
            for i in range(recharge_count):
                nodes.append(graph.insert_vertex(f"R{i}", node_type="recarga"))
            for i in range(client_count):
                nodes.append(graph.insert_vertex(f"C{i}", node_type="cliente"))

            # Garantizar conectividad (árbol base)
            random.shuffle(nodes)
            for i in range(1, len(nodes)):
                weight = random.randint(1, 20)
                graph.insert_edge(nodes[i-1], nodes[i], weight)
                graph.insert_edge(nodes[i], nodes[i-1], weight)

            # Aristas adicionales hasta completar m_edges
            remaining_edges = n_edges - (n_nodes - 1)
            while remaining_edges > 0:
                u, v = random.sample(nodes, 2)
                if not graph.get_edge(u, v):
                    weight = random.randint(1, 20)
                    graph.insert_edge(u, v, weight)
                    graph.insert_edge(v, u, weight)
                    remaining_edges -= 1

            # Elegir nodos cliente como origen y destino
            cliente_nodos = [v for v in graph.vertices() if v.type == "cliente"]
            if len(cliente_nodos) < 2:
                st.error("No hay suficientes nodos cliente para simular rutas.")
            else:
                origen_v = random.choice(cliente_nodos)
                destino_v = random.choice([v for v in cliente_nodos if v != origen_v])
                origin = origen_v.element()
                destination = destino_v.element()

                # Prioridad aleatoria
                priority = random.randint(1, 3)

                # Ejecutar simulación
                result = run_simulation(origin, destination, priority)

                if result.get("ruta"):
                    st.success(f"✅ Ruta encontrada desde {origin} hasta {destination} (Prioridad: {priority})")
                    st.json(result)

                    # Crear orden
                    order_id = len(st.session_state["ordenes"]) + 1
                    orden = Order(
                        order_id=order_id,
                        client_id=destination,
                        origin=origin,
                        destination=destination,
                        path=result["ruta"],
                        cost=result["costo"],
                        priority=priority
                    )
                    st.session_state["ordenes"].append(orden)

                    # Registrar cliente
                    cid = destination
                    if cid not in st.session_state["clientes"]:
                        st.session_state["clientes"][cid] = Client(cid, f"Cliente {cid}", cid)
                    st.session_state["clientes"][cid].incremento_ordenes()
                else:
                    st.error("❌ No se pudo calcular una ruta válida con la autonomía del dron.")



    # ----------------------- 2. Visualización -----------------------
    with tabs[1]:
        st.header("🗺️ Visualización de Rutas")
        st.info("Aquí puedes visualizar el mapa de nodos y las rutas calculadas.")
        st.warning("🚧 Visualización gráfica en construcción...")

    # ----------------------- 3. Clientes -----------------------
    with tabs[2]:
        st.header("👤 Gestión de Clientes")
        st.info("Información relacionada a los clientes y su historial de pedidos.")

        # Mostrar clientes registrados
        if "clientes" in st.session_state and st.session_state["clientes"]:
            for cliente_id, cliente_obj in st.session_state["clientes"].items():
                st.subheader(f"🧍 Cliente {cliente_id}")
                st.json(cliente_obj.to_dict())
        else:
            st.warning("No hay clientes registrados aún. Ejecuta una simulación primero.")

    # ----------------------- 4. Órdenes -----------------------
    with tabs[3]:
        st.header("📦 Órdenes y Estados")
        st.info("Lista de órdenes con su origen, destino, estado y prioridad.")

        if st.session_state["ordenes"]:
            for orden in st.session_state["ordenes"]:
                st.json(orden.to_dict())
        else:
            st.warning("No hay órdenes registradas todavía.")

    # ----------------------- 5. Estadísticas -----------------------
    with tabs[4]:
        st.header("📊 Estadísticas del Sistema")
        st.info("Frecuencia de uso de nodos, rutas frecuentes, y análisis de entregas.")
        st.warning("🚧 Gráficas en desarrollo...")

# ------------------------- MAIN -------------------------
if __name__ == "__main__":
    main()
