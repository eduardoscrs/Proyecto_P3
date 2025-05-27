# 🛰️ Sistema Logístico Autónomo con Drones

**Asignatura:** INFO1126 - Programación 3  

---

## 📦 Descripción del Proyecto

Este proyecto simula un sistema de entrega autónoma con drones para la empresa **Correos Chile**, diseñado para superar las limitaciones del transporte terrestre. El sistema considera:

- Nodos de almacenamiento, recarga y clientes.
- Autonomía energética de los drones.
- Generación y análisis de rutas en grafos conectados.
- Visualización e interacción completa mediante Streamlit.

---

## 🎯 Objetivos

- Generar y simular una red logística con drones autónomos.
- Planificar rutas que respeten la autonomía del dron.
- Analizar las rutas y nodos más utiSlizados mediante un AVL.
- Visualizar y operar el sistema desde una interfaz interactiva.

---

## ⚙️ Funcionalidades principales

| Pestaña | Funcionalidad |
|--------|----------------|
| 🔄 **Run Simulation** | Configurar y generar un entorno de simulación personalizado. |
| 🌍 **Explore Network** | Calcular rutas entre nodos considerando autonomía y recarga. |
| 🌐 **Clients & Orders** | Visualizar clientes, órdenes y su historial. |
| 📋 **Route Analytics** | Mostrar rutas más usadas y AVL de recorridos. |
| 📈 **General Statistics** | Estadísticas globales del sistema: uso de nodos y roles. |

---

## 📊 Parámetros de Simulación

- Máximo de nodos: **150**
- Distribución:
  - 📦 Almacenamiento: 20%
  - 🔋 Recarga: 20%
  - 👤 Clientes: 60%
- Autonomía máxima del dron: **50 unidades de costo**
- Estructuras usadas: **Grafo, AVL, Hash Map propio**

---

## 🧠 Algoritmos y Estructuras

- **BFS / DFS / Topological Sort** para rutas.
- **AVL Tree** para registrar rutas más frecuentes.
- **Hash Map** propio para acceder a clientes y órdenes en O(1).
- Generación de grafos conexos evitando nodos aislados.

---

## 🗂️ Estructura del Proyecto

└── Proyect
    ├── domain
    │   ├── client.py
    │   ├── order.py
    │   └── route.py
    ├── model
    │   ├── __init__.py
    │   ├── edge.py
    │   ├── graph.py
    │   └── vertex.py
    ├── sim
    │   ├── init_simulation.py
    │   └── simulation.py
    ├── tda
    │   ├── avl.py
    │   └── hasp_map.py
    └── visual
        ├── avl_visualizer.py
        ├── dashboard.py
        └── networkx_adapter.py

---

## ✅ Estado del Proyecto

- [ ] Generación dinámica de grafos
- [ ] Algoritmo de rutas con límite de batería
- [ ] AVL para rutas más frecuentes
- [ ] Interfaz Streamlit funcional con 5 pestañas
- [ ] Estadísticas generales
- [ ] Pruebas y validaciones

---

## 🛤️ Ruta de Desarrollo 

1. **Estructura base del grafo**
   - [ ] `Graph`, `Vertex`, `Edge` con roles.
   - [ ] Generador de grafos conexos (mínimo n-1 aristas).

2. **Controlador de simulación**
   - [ ] Inicialización de nodos y asignación de roles.
   - [ ] Generación de órdenes.

3. **Algoritmos de búsqueda**
   - [ ] Implementar BFS, DFS y Topological Sort con límite de batería.

4. **Rutas y AVL**
   - [ ] Clase `Route` con trazado y costo.
   - [ ] Registrar rutas en AVL e incrementar frecuencia.

5. **Interfaz en Streamlit**
   - [ ] Pestaña 1: Configuración y generación del entorno.
   - [ ] Pestaña 2: Cálculo de rutas con visualización.
   - [ ] Pestaña 3: Clientes y órdenes.
   - [ ] Pestaña 4: Análisis AVL de rutas.
   - [ ] Pestaña 5: Estadísticas generales.

6. **Pruebas finales y presentación**
   - [ ] Validar conectividad.
   - [ ] Validar rutas según autonomía.
   - [ ] Documentar código y preparar presentación.

---

## 📎 Recursos

- 📹 [Guía en video](https://youtu.be/AXj14zeKqTI)
- 📝 [PDF del proyecto](Proyecto%201%20-%20Info%201126.pdf)
