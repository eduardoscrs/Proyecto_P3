import streamlit as st
from Proyect.sim.simulation import run_simulation
from Proyect.data.map_data import NODES  # Asegúrate que este archivo contenga las ciudades posibles

def main():
    st.set_page_config(page_title="Simulación de Entregas", layout="wide")
    st.title("📦 Dashboard de Simulación Logística")

    st.write("Este panel permite simular entregas entre distintos puntos del mapa.")

    # Parámetros de simulación
    st.subheader("🔧 Parámetros de Simulación")

    col1, col2, col3 = st.columns(3)
    with col1:
        origin = st.selectbox("Ciudad origen", NODES)
    with col2:
        destination = st.selectbox("Ciudad destino", NODES, index=1)
    with col3:
        priority = st.select_slider("Prioridad del pedido", options=[1, 2, 3], value=1)

    if origin == destination:
        st.warning("El origen y destino no pueden ser iguales.")
        return

    if st.button("🚀 Ejecutar Simulación"):
        with st.spinner("Simulando entrega..."):
            result = run_simulation(origin, destination, priority)
            st.success("✅ Simulación completada")

            # Mostrar resultados
            st.subheader("📋 Resultados")
            st.json(result)

            # (Opcional) Mostrar ruta
            if "path" in result:
                st.write("Ruta calculada:")
                st.write(" ➡️ ".join(result["path"]))

if __name__ == "__main__":
    main()
