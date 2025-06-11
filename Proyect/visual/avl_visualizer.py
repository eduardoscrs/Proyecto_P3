import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st

def draw_avl_tree(avl_tree, title="AVL Tree Visualization"):
    """
    Visualiza un AVLTree como grafo usando networkx y matplotlib en Streamlit.
    Requiere que avl_tree tenga un método .to_networkx() que devuelva un DiGraph.
    """
    if not avl_tree or not avl_tree.root:
        st.info("El árbol AVL está vacío.")
        return

    G = avl_tree.to_networkx()

    try:
        pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
    except:
        pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_color="#8ecae6", node_size=1800, font_size=9)
    plt.title(title)
    st.pyplot(plt.gcf())
