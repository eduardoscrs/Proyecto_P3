import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.patches import Patch

def draw_network(nx_graph, path=None):
    """
    Función para dibujar el grafo de NetworkX usando Matplotlib.
    
    :param nx_graph: Grafo de NetworkX con nodos y aristas
    :param path: Ruta opcional para resaltar en el grafo (si existe)
    """
    tipo_color = {
        "almacenamiento": "#f39c12",
        "recarga": "#3498db",
        "cliente": "#2ecc71"
    }

    num_nodes = nx_graph.number_of_nodes()

    try:
        # Elegir el layout adecuado en función del tamaño del grafo
        if num_nodes <= 30:
            pos = nx.spring_layout(nx_graph, seed=42)
        elif num_nodes <= 100:
            pos = nx.kamada_kawai_layout(nx_graph)
        else:
            pos = nx.shell_layout(nx_graph)
    except:
        pos = nx.spring_layout(nx_graph, seed=42)

    # Colores de los nodos
    node_colors = [tipo_color.get(nx_graph.nodes[n].get("tipo", ""), "#95a5a6") for n in nx_graph.nodes]
    
    # Colores de las aristas (resaltar las aristas de la ruta si se proporcionan)
    edge_colors = ["red" if path and (u, v) in zip(path, path[1:]) else "gray" for u, v in nx_graph.edges]

    # Tamaño de los nodos en función del número de nodos
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

    # Etiquetas de las aristas (peso de la arista)
    if num_nodes <= 50:
        edge_labels = nx.get_edge_attributes(nx_graph, 'weight')
        nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels=edge_labels, font_size=font_size)

    # Leyenda
    legend_elements = [
        Patch(facecolor=tipo_color["almacenamiento"], label="Storage"),
        Patch(facecolor=tipo_color["recarga"], label="Recharge"),
        Patch(facecolor=tipo_color["cliente"], label="Client"),
    ]
    plt.legend(handles=legend_elements, loc="lower left", fontsize=font_size + 1)

    # Mostrar el grafo en Streamlit
    st.pyplot(plt.gcf())

def draw_mst(mst):
    """
    Dibuja el Árbol de Expansión Mínima (MST) calculado por Kruskal.
    
    :param mst: Árbol de expansión mínima (MST) de NetworkX
    """
    pos = nx.spring_layout(mst)
    plt.figure(figsize=(12, 9))
    nx.draw(mst, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=10, font_weight='bold')
    plt.title("Árbol de Expansión Mínima")
    st.pyplot(plt.gcf())

def convert_to_json(nx_graph):
    """
    Convierte el grafo de NetworkX a un formato JSON para facilitar su transmisión a través de la API.
    
    :param nx_graph: Grafo de NetworkX con nodos y aristas
    :return: Diccionario con nodos y aristas para JSON
    """
    nodes = [{"node": n, "type": nx_graph.nodes[n]["tipo"]} for n in nx_graph.nodes]
    edges = [{"source": u, "target": v, "weight": nx_graph[u][v]["weight"]} for u, v in nx_graph.edges]
    
    return {"nodes": nodes, "edges": edges}

def draw_route(nx_graph, route):
    """
    Dibuja la ruta más corta en el grafo resaltando las aristas que pertenecen a la ruta.
    
    :param nx_graph: Grafo de NetworkX con nodos y aristas
    :param route: Lista de nodos que forman la ruta más corta
    """
    # Resaltar los nodos y aristas de la ruta
    path_edges = list(zip(route[:-1], route[1:]))
    edge_colors = ["red" if (u, v) in path_edges or (v, u) in path_edges else "gray" for u, v in nx_graph.edges]
    
    pos = nx.spring_layout(nx_graph)
    plt.figure(figsize=(12, 9))
    nx.draw(nx_graph, pos, with_labels=True, node_size=800, edge_color=edge_colors, font_size=10, font_weight='bold')
    st.pyplot(plt.gcf())

