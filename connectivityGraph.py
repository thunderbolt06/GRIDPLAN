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
        f = plt.Figure(figsize=(3, 3), dpi=100)
        ax = f.add_subplot(111)
        g = nx.Graph()
        g.add_edges_from(app.game_data.adjacency_list)
        # nx.draw(g, pos=nx.spectral_layout(g), ax=ax, with_labels=True, node_color="#ADD8E6")
        nx.draw(g, pos=nx.spring_layout(g), ax=ax, with_labels=True, node_color="#ADD8E6")
        # nx.draw_planar(g, ax=ax, with_labels=True, node_color="#ADD8E6")
        canvas = FigureCanvasTkAgg(f, app.connectivity_graph_frame)

        app.connectivity_graph_canvas = canvas.get_tk_widget()
        app.connectivity_graph_canvas.grid(row=0,column=0)
        print(app.connectivity_graph_canvas, "canv")
