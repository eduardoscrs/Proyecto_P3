# Proyect/visual/dashboard.py
import streamlit as st
from Proyect.sim.simulation import run_simulation

def main():
    st.set_page_config(page_title="Simulación", layout="wide")
    st.title("Dashboard de Simulación")

    st.write("Este es el panel visual del proyecto.")

    if st.button("Ejecutar simulación"):
        results = run_simulation()
        st.success("Simulación completada")
        st.json(results)

if __name__ == "__main__":
    main()
