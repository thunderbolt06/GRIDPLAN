import tkinter as tk
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from constants import *

class ConnectivityGraph:
    def create_connectivity_graph(app):
        title = tk.Canvas(app.connectivity_graph_frame, width=app.screen_width/4, height=app.screen_height/2)
        title.grid()
        title.create_text(100, 50, text="Connectivity", font=helv8)
        app.f = plt.Figure(figsize=(3, 3), dpi=100)
        app.ax = app.f.add_subplot(111)
        app.graph.clear()
        app.graph.add_edges_from(app.game_data.adjacency_list, color='grey')
        print(app.game_data.current_box_adjacency)
        attrs = {(i, j): {"color": 'green'} for i,j in app.game_data.current_box_adjacency}
        nx.set_edge_attributes(app.graph, attrs)
        colors = [app.graph[u][v]['color'] for u,v in app.graph.edges()]
        # nx.draw(g, pos=nx.spectral_layout(g), ax=ax, with_labels=True, node_color="#ADD8E6")
        nx.draw(app.graph, pos=nx.spring_layout(app.graph), ax=app.ax, with_labels=True,
                 node_color="#ADD8E6", edge_color=colors)
        # nx.draw_planar(g, ax=ax, with_labels=True, node_color="#ADD8E6")
        canvas = FigureCanvasTkAgg(app.f, app.connectivity_graph_frame)

        app.connectivity_graph_canvas = canvas.get_tk_widget()
        app.connectivity_graph_canvas.grid(row=0,column=0)
        print(app.connectivity_graph_canvas, "canv")

    def refresh_connectivity_graph(app):
        print("refresh called")
        plt.clf()
        app.connectivity_graph_canvas.destroy()
        app.ax.remove()
        app.ax = app.f.add_subplot(111)
        attrs = {(i, j): {"color": 'green'} for i,j in app.game_data.current_box_adjacency}
        nx.set_edge_attributes(app.graph, attrs)

        colors = [app.graph[u][v]['color'] for u,v in app.graph.edges()]
        nx.draw(app.graph, pos=nx.spring_layout(app.graph), ax=app.ax, with_labels=True,
                 node_color="#ADD8E6", edge_color=colors, width=2)

        canvas = FigureCanvasTkAgg(app.f, app.connectivity_graph_frame)

        app.connectivity_graph_canvas = canvas.get_tk_widget()
        app.connectivity_graph_canvas.grid(row=0,column=0)
