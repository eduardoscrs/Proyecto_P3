import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st

def hierarchy_pos(G, root=None, width=1.0, vert_gap=0.3, vert_loc=0, xcenter=0.5, pos=None, parent=None):
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    children = list(G.successors(root))
    if len(children) != 0:
        dx = width / len(children)
        nextx = xcenter - width/2 - dx/2
        for child in children:
            nextx += dx
            pos = hierarchy_pos(G, root=child, width=dx, vert_gap=vert_gap,
                                vert_loc=vert_loc - vert_gap, xcenter=nextx, pos=pos, parent=root)
    return pos

def draw_avl_tree(avl_tree, title="AVL Tree Visualization"):
    if avl_tree.root is None:
        st.info("Árbol AVL vacío.")
        return

    G = avl_tree.to_networkx()
    labels = nx.get_node_attributes(G, "label")
    root_label = str(avl_tree.root.key)

    try:
        pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
    except:
        # st.warning("⚠️ No se encontró Graphviz, usando layout jerárquico alternativo.")
        try:
            pos = hierarchy_pos(G, root=root_label)
        except:
            st.error("No se pudo generar una posición jerárquica para el árbol.")
            return

    fig, ax = plt.subplots(figsize=(12, 6))
    nx.draw(G, pos, with_labels=True, labels=labels,
            node_color="#8ecae6", node_size=1800, font_size=9, ax=ax)
    plt.title(title)
    st.pyplot(fig)

    # Exportar como PNG
    if st.button("📸 Export AVL Tree as PNG"):
        fig.savefig("avl_tree.png")
        with open("avl_tree.png", "rb") as f:
            st.download_button("⬇️ Download AVL Tree", f, file_name="avl_tree.png", mime="image/png")
