import streamlit as st
from Proyect.sim.simulation import run_simulation
from Proyect.data.map_data import NODES

def main():
    st.set_page_config(page_title="Simulación de Rutas", layout="wide")
    st.title("📦 Simulador de Rutas de Entrega")

    st.markdown("""
    Bienvenido al sistema de simulación logística. Aquí puedes crear simulaciones, visualizar rutas, consultar clientes, órdenes, y revisar estadísticas del sistema.
    """)

    tabs = st.tabs(["🔁 Simulación", "🗺️ Visualización", "👤 Clientes", "📦 Órdenes", "📊 Estadísticas"])

    # ----------------------- 1. Simulación -----------------------
    with tabs[0]:
        st.header("🔁 Crear Simulación")

        origin = st.selectbox("Selecciona nodo de origen", NODES)
        destination = st.selectbox("Selecciona nodo de destino", NODES, index=1)
        priority = st.slider("Prioridad del pedido", 1, 3, 1)

        if origin == destination:
            st.warning("⚠️ El origen y destino deben ser distintos.")
        elif st.button("🚀 Ejecutar Simulación"):
            result = run_simulation(origin, destination, priority)
            st.success("✅ Simulación completada")
            st.json(result)

    # ----------------------- 2. Visualización -----------------------
    with tabs[1]:
        st.header("🗺️ Visualización de Rutas")
        st.info("Aquí puedes visualizar el mapa de nodos y las rutas calculadas.")
        # Aquí iría visualización con networkx o matplotlib

    # ----------------------- 3. Clientes -----------------------
    with tabs[2]:
        st.header("👤 Gestión de Clientes")
        st.info("Información relacionada a los clientes y su historial de pedidos.")
        # Mostrar clientes y detalles

    # ----------------------- 4. Órdenes -----------------------
    with tabs[3]:
        st.header("📦 Órdenes y Estados")
        st.info("Lista de órdenes con su origen, destino, estado y prioridad.")
        # Mostrar tabla con órdenes

    # ----------------------- 5. Estadísticas -----------------------
    with tabs[4]:
        st.header("📊 Estadísticas del Sistema")
        st.info("Frecuencia de uso de nodos, rutas frecuentes, y análisis de entregas.")
        # Gráficos con matplotlib o plotly

if __name__ == "__main__":
    main()
