import tkinter as tk
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

helv15 = ("Helvetica", 15, "bold")
helv8 = ("Helvetica", 8, "bold")
colors = [
    "#7B68EE",  # medium slate blue
    "#40E0D0",  # turqouise
    "#FF7F50",  # coral
    "#FF69B4",  # hot pink
    "#e3099e",  # lavender
    "#FA8072",  # salmon
    "#98FB98",  # pale green
    "#BA55D3",  # medium orchid
    "#B0C4DE",  # light steel blue
    "#FFA500",  # orange
    "#FFDAB9",  # peach puff
    "#6495ED",  # corn flower blue
] * 10
INPUTGRAPH_JSON_PATH = ("./FastPLAN/inputgraph.json")

rgb_colors = [
    (123, 104, 238),  # medium slate blue
    (64, 224, 208),  # turqouise
    (255, 127, 80),  # coral
    (255, 105, 180),  # hot pink
    (230, 230, 250),  # lavender
    (250, 128, 114),  # salmon
    (152, 251, 152),  # pale green
    (186, 85, 211),  # medium orchid
    (176, 196, 222),  # light steel blue
    (255, 165, 0),  # orange
    (255, 218, 185),  # peach puff
    (100, 149, 237),  # corn flower blue
]*10

hex_colors = [
    "#7B68EE",  # medium slate blue
    "#40E0D0",  # turqouise
    "#FF7F50",  # coral
    "#FF69B4",  # hot pink
    "#e3099e",  # lavender
    "#FA8072",  # salmon
    "#98FB98",  # pale green
    "#BA55D3",  # medium orchid
    "#B0C4DE",  # light steel blue
    "#FFA500",  # orange
    "#FFDAB9",  # peach puff
    "#6495ED",  # corn flower blue
]*10


class GameData:
    def __init__(self) -> None:
        self.adjacency_graph = [[0,1], [1,2], [2,0]]
        self.box_sizes = [[1,1], [1,1], [2,1], [1,1], [1,1], [2,1]]

        self.rfp = None
        self.grid_row_size = 5
        self.grid_col_size = 4

class App:
    def __init__(self) -> None:
        self.gameData()
        self.initialise_root()
        self.title_section()
        self.connectivity_graph_section()
        self.user_grid_section()
        self.inventory_section()
        self.buttons_section()

    def gameData(self):
        self.game_data = GameData()

    def connectivity_graph_section(self):
        self.connectivity_graph_frame = tk.Frame(self.root, width=self.screen_width/4, height=self.screen_height/2, highlightbackground="blue", highlightthickness=2)
        self.connectivity_graph_frame.grid(row=1, column=0)

        title = tk.Canvas(self.connectivity_graph_frame, width=self.screen_width/4, height=self.screen_height/2)
        title.grid()
        title.create_text(50, 50, text="Connectivity")
        f = plt.Figure(figsize=(3, 3), dpi=100)
        ax = f.add_subplot(111)
        g = nx.Graph()
        g.add_edges_from(self.game_data.adjacency_graph)
        nx.draw(g, ax=ax, with_labels=True, node_color="#ADD8E6")
        canvas = FigureCanvasTkAgg(f, self.connectivity_graph_frame)

        self.connectivity_graph_canvas = canvas.get_tk_widget()
        self.connectivity_graph_canvas.grid(row=0,column=0)
        print(self.connectivity_graph_canvas, "canv")



    def user_grid_section(self):
        
        self.user_grid_frame = tk.Frame(self.root, width=self.screen_width*0.7, height=self.screen_height/2, highlightbackground="blue", highlightthickness=2)
        self.user_grid_frame.grid(row=1, column=1)
        title = tk.Label(self.user_grid_frame, text="User Grid")
        title.place(x = 100, y = 50)
        self.create_bg_grid(self.game_data.grid_row_size, self.game_data.grid_col_size, self.user_grid_frame)

        # title = tk.Label(self.user_grid_frame, text="asdf")
        # title.place(x = 100 , y = 99)
        # self.user_grid_canvas = tk.Canvas(self.user_grid_frame, width=self.screen_width/3, height=self.screen_height/2)
        # self.user_grid_canvas.grid()
        # self.user_grid_canvas.create_text(50, 50, text="User Grid")

    def create_bg_grid(self, row, col, frame):
        
        for r in range(row):
            for c in range(col):
                title = tk.Frame(self.user_grid_frame, highlightbackground="light grey", highlightthickness=1, width=50, height=50)
                title.place(x = 100 + c*50 , y = 100 + 50*r)
        pass

    def drag_start(self, event, label):
        label.startX = event.x
        label.startY = event.y

    def drag_motion(self, event, label):
        x = min(max(label.winfo_x() - label.startX + event.x, self.user_grid_frame.winfo_x()), self.user_grid_frame.winfo_x() + self.user_grid_frame.winfo_width() - label.winfo_width())
        y = min(max(label.winfo_y() - label.startY + event.y, self.user_grid_frame.winfo_y()), self.user_grid_frame.winfo_y() + self.user_grid_frame.winfo_height() - label.winfo_height())

        print(x)
        print(y)
        user_grid_frame_x = self.user_grid_frame.winfo_x()
        user_grid_frame_y = self.user_grid_frame.winfo_y()

        if(x > user_grid_frame_x + 100 and x < user_grid_frame_x + 100 + 50 * (self.game_data.grid_col_size)
           and y > user_grid_frame_y + 100 and y < user_grid_frame_y + 100 + 50 * (self.game_data.grid_row_size)):
            x = ((x - 100 - user_grid_frame_x) // 50) * 50 + 100 + user_grid_frame_x
            y = ((y - 100 - user_grid_frame_y) // 50) * 50 + 100 + user_grid_frame_y

        label.place(x = x, y = y)

    def inventory_section(self):
        title = tk.Label(self.user_grid_frame, text="Boxes")
        title.place(x = 500, y = 50)

        cur_x = 500
        cur_y = 100

        for i in range(len(self.game_data.box_sizes)):
            title = tk.Frame(self.user_grid_frame, highlightthickness=2, width=50*self.game_data.box_sizes[i][0], height=50*self.game_data.box_sizes[i][1], bg=hex_colors[i])
            title.place(x = cur_x, y = cur_y)
            # label = tk.Label(title, text=i)
            # label.grid()
            cur_x += 150
            if(cur_x > 1000):
                cur_x = 500
                cur_y += 150
        pass
        # self.inventory_frame = tk.Frame(self.root, width=self.screen_width/3, height=self.screen_height, highlightbackground="blue", highlightthickness=2)
        # self.inventory_frame.grid(row=1, column=2)
        # self.inventory_canvas = tk.Canvas(self.inventory_frame, width=self.screen_width/3, height=self.screen_height/2)
        # self.inventory_canvas.grid()
        # self.inventory_canvas.create_text(50, 50, text="Boxes")

        self.boxes = {}
        # rect = self.inventory_frame(50, 110,300,280, fill= "light blue")
        label = tk.Frame(self.root, bg="red", width=100, height=100)
        label.place(x= 900, y = 200)
        label.bind("<Button-1>", lambda event : self.drag_start(event, label))
        label.bind("<B1-Motion>", lambda event : self.drag_motion(event, label))
        # self.boxes[rect] = {}
        # self.inventory_canvas.tag_bind(rect, "<Button-1>", lambda event : self.drag_start(event, rect, self.inventory_canvas))
        # self.inventory_canvas.tag_bind(rect, "<Button-1>", lambda x: print("hello"))
        # self.inventory_canvas.tag_bind(rect, "<B1-Motion>", lambda event : self.drag_motion(event, rect, self.inventory_canvas))
        # self.inventory_canvas.bind("<B1-Motion>", lambda event : self.drag_motion(event, rect))

    # def drag_start(self, event, rect, canvas):
    #     print(rect)
    #     print(canvas.coords(rect))
    #     self.boxes[rect]["startX"] = event.x
    #     self.boxes[rect]["startY"] = event.y
    #     # rect.startX = event.x
    #     # rect.startY = event.y

    # def drag_motion(self, event, rect, canvas):
    #     # x = rect.winfo_x() - rect.startX + event.X
    #     # y = rect.winfo_Y() - rect.startY + event.y
    #     # rect.place(x=x, y=y)
    #     pass

        
    def buttons_section(self):
        
        self.connectivity_graph_frame = tk.Frame(self.root, width=self.screen_width/2, height=self.screen_height/10, highlightbackground="blue", highlightthickness=2)
        self.connectivity_graph_frame.grid(row=2, column=0, columnspan=3)

        self.create_btn = tk.Button(self.connectivity_graph_frame, text="Create new")
        self.create_btn.grid()

        self.submit_btn = tk.Button(self.connectivity_graph_frame, text="Submit")
        self.submit_btn.grid()

        self.clear_btn = tk.Button(self.connectivity_graph_frame, text="Clear")
        self.clear_btn.grid()

    def run(self):
        self.root.mainloop()

    def initialise_root(self):
        self.root = tk.Tk()
        self.root.title("Rule Based GPLAN")
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(str(str(self.screen_width) +
                           'x' + str(self.screen_height)))

    def title_section(self):
        self.logo_frame = tk.Frame(self.root, highlightbackground="blue", highlightthickness=2)
        self.logo_frame.grid(row=0, column=0,columnspan=3)
        logo_canvas = tk.Canvas(self.logo_frame, width=self.screen_width*0.9, height=100)
        logo_canvas.pack()
        logo_canvas.create_text(50, 50, text="GPLAN", font=helv15)


    def checkered(canvas, line_distance):
        # vertical lines at an interval of "line_distance" pixel
        for x in range(line_distance,canvas_width,line_distance):
            canvas.create_line(x, 0, x, canvas_height, fill="#476042")
        # horizontal lines at an interval of "line_distance" pixel
        for y in range(line_distance,canvas_height,line_distance):
            canvas.create_line(0, y, canvas_width, y, fill="#476042")



def run():
    app = App()
    app.run()


if __name__ == "__main__":
    app = App()
    app.run()

