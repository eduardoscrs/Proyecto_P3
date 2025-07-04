from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd

def generate_pdf_report(sim_data, avl_tree):
    buffer = BytesIO()
    with PdfPages(buffer) as pdf:
        fig, ax = plt.subplots(figsize=(8.27, 11.69))
        ax.axis("off")
        ax.set_title("📄 Informe del Sistema Logístico Autónomo", fontsize=16, weight='bold', pad=20)
        ax.text(0, 0.8, "Resumen General del Sistema", fontsize=12)
        ax.text(0, 0.75, f"Nodos de Almacenamiento: {len(sim_data['storage_nodes'])}")
        ax.text(0, 0.72, f"Nodos de Recarga: {len(sim_data['recharge_nodes'])}")
        ax.text(0, 0.69, f"Nodos de Clientes: {len(sim_data['client_nodes'])}")
        ax.text(0, 0.63, "Cantidad de Órdenes: {}".format(len(sim_data['orders'])))
        pdf.savefig(fig)
        plt.close()

        fig, ax = plt.subplots(figsize=(8.27, 11))
        ax.axis("off")
        ax.set_title("🌿 Rutas más frecuentes (AVL)", fontsize=14, weight='bold')
        # Usar la lista serializada directamente
        top_routes = avl_tree[:10] if isinstance(avl_tree, list) else avl_tree.get_top_routes(10)
        y = 0.9
        for i, (ruta, freq) in enumerate(top_routes, 1):
            ax.text(0.1, y, f"{i}. {ruta} → Freq: {freq}", fontsize=10)
            y -= 0.05
        pdf.savefig(fig)
        plt.close()

        fig, ax = plt.subplots(figsize=(8, 6))
        clients = sim_data["clientes"]
        # Adaptar para dicts serializados
        client_orders = {cid: c["total_orders"] for cid, c in clients.items() if isinstance(c, dict) and "total_orders" in c}
        df_clients = pd.DataFrame(list(client_orders.items()), columns=["Cliente", "Pedidos"])
        df_clients.sort_values("Pedidos", ascending=False, inplace=True)
        df_clients.head(10).plot(kind="bar", x="Cliente", y="Pedidos", ax=ax, legend=False, color="green")
        ax.set_title("👤 Clientes más recurrentes")
        pdf.savefig(fig)
        plt.close()

        fig, axs = plt.subplots(1, 3, figsize=(10, 4))
        axs = axs.flatten()
        edge_list = sim_data["edge_list"] if "edge_list" in sim_data else []
        recharge_usage = {n: sum(1 for e in edge_list if e["source"] == n or e["target"] == n) for n in sim_data["recharge_nodes"]}
        pd.Series(recharge_usage).sort_values(ascending=False).head(5).plot(kind="bar", ax=axs[0], color="blue", title="🔋 Recarga")
        storage_usage = {n: sum(1 for e in edge_list if e["source"] == n or e["target"] == n) for n in sim_data["storage_nodes"]}
        pd.Series(storage_usage).sort_values(ascending=False).head(5).plot(kind="bar", ax=axs[1], color="orange", title="📦 Almacenamiento")
        client_usage = {n: sum(1 for e in edge_list if e["source"] == n or e["target"] == n) for n in sim_data["client_nodes"]}
        pd.Series(client_usage).sort_values(ascending=False).head(5).plot(kind="bar", ax=axs[2], color="green", title="👤 Clientes")
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close()

        fig, ax = plt.subplots(figsize=(6, 6))
        labels = ['Storage', 'Recharge', 'Client']
        values = [len(sim_data["storage_nodes"]), len(sim_data["recharge_nodes"]), len(sim_data["client_nodes"])]
        colors = ['orange', 'blue', 'green']
        ax.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.set_title("Distribución de roles de nodos")
        pdf.savefig(fig)
        plt.close()

    buffer.seek(0)
    return buffer.getvalue()
