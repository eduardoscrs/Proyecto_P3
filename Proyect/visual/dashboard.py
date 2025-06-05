import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    # Aquí cargas los datos, por ejemplo desde CSV o base de datos
    # df = pd.read_csv("data.csv")
    # return df
    return pd.DataFrame({
        "categoría": ["A", "B", "C"],
        "valor": [100, 200, 150]
    })

def show_chart(df):
    st.subheader("Gráfico de valores")
    fig, ax = plt.subplots()
    ax.bar(df["categoría"], df["valor"])
    st.pyplot(fig)

def main():
    st.title("Dashboard del Proyecto P3")
    df = load_data()

    st.dataframe(df)

    if st.checkbox("Mostrar gráfico"):
        show_chart(df)

    st.success("Dashboard cargado correctamente.")

if __name__ == "__main__":
    main()
