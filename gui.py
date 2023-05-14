import tkinter as tk
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import json
from collections import namedtuple

helv15 = ("Helvetica", 30, "bold")
helv8 = ("Helvetica", 20, "bold")
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

 
# customDecoder function
def customDecoder(obj):
    return namedtuple('X', obj.keys())(*obj.values())

class GameData:
    def __init__(self, level) -> None:
        file_name = f"./level{level}.json"
        file = open(file_name)
        json_data = json.load(file, object_hook = customDecoder)
        self.adjacency_list= json_data.adjacency_list
        self.box_sizes= json_data.box_sizes
        
        
        self.grid_row_size = json_data.grid_row_size
        self.grid_col_size = json_data.grid_col_size
        # self.adjacency_list = [[0,1], [1,2], [2,0]]
        # self.box_sizes = [[1,1], [1,1], [2,1]]
        self.num_boxes = len(self.box_sizes)
        self.init_graph = nx.Graph()
        self.init_graph.add_edges_from(self.adjacency_list)
        self.width_quanta = 50
        self.height_quanta = 50
        self.rfp = None
        self.box_frames = [tk.Frame] * 10
        self.boxes_init_x = [0] * 10
        self.boxes_init_y = [0] * 10
        self.boxes_cur_x = [0] * 10
        self.boxes_cur_y = [0] * 10
        self.current_box_graph = nx.Graph()
        self.grid_coords = [100, 100, self.grid_col_size*50, self.grid_row_size*50]
        

        self.current_box_adjacency = []
        self.current_box_graph.add_edges_from(self.current_box_adjacency)

    def check_two_boxes_adjacent(self, x1, y1, w1, h1, x2, y2, w2, h2):
        if(
            (
                # Horizontally adjacent
                ( x1 + w1 == x2 or x2 + w2 == x1 ) and
                y2 + h2 > y1 and
                y2 < y1 + h1
            )
            or 
            (
                # Vertically adjacent
                ( y1 + h1 == y2 or y2 + h2 == y1 ) and
                x2 + w2 > x1 and
                x2 < x1 + w1
            )
        ):
            return True
        else:
            return False
    def get_current_box_adjacency(self):
        self.current_box_adjacency = []
        for i in range(self.num_boxes):
            for j in range(self.num_boxes):
                if(i < j):
                    print("adj for", i, j)
                    if( self.check_two_boxes_adjacent(self.boxes_cur_x[i], self.boxes_cur_y[i], self.width_quanta*self.box_sizes[i][0],self.height_quanta*self.box_sizes[i][1]
                                                      , self.boxes_cur_x[j], self.boxes_cur_y[j], self.width_quanta*self.box_sizes[j][0],self.height_quanta*self.box_sizes[j][1] )):
                        self.current_box_adjacency.append([i,j])
                        print(i,j, "are adjacent")      
                    print(self.boxes_cur_x[i], self.boxes_cur_y[i])
                    print(self.boxes_cur_x[j], self.boxes_cur_y[j])
                    pass
        self.current_box_graph.clear()
        self.current_box_graph.add_edges_from(self.current_box_adjacency)
    
    def check_game_success(self, label):
        if(self.check_if_box_satisfy_adj() and self.check_if_all_boxes_are_inside_grid()):
            
            label.config(text="Congratulations!!! You have completed the level")
        else :
            label.config(text="Incorrect!! please try again")

    def check_one_box_is_inside_grid(self,x, y, w, h):

        if(x >= self.grid_coords[0] and 
           y >= self.grid_coords[1] and 
           x + w <= self.grid_coords[0] + self.grid_coords[2] and 
           y + h <= self.grid_coords[1] + self.grid_coords[3]):
            return True
        print("this box is out of grid")
        print(x, y , w , h)
        print(self.grid_coords)
        return False

    def check_if_all_boxes_are_inside_grid(self):
        print("checking if boxes are inside grid")
        for i in range(self.num_boxes):
            if(self.check_one_box_is_inside_grid(self.boxes_cur_x[i], self.boxes_cur_y[i], self.width_quanta*self.box_sizes[i][0],self.height_quanta*self.box_sizes[i][1] ) == False):
                print(i, "is not inside the grid")
                return False
        print("all boxes are inside the grid")
        return True

    def check_if_box_satisfy_adj(self):
        self.get_current_box_adjacency()
        print(self.current_box_graph.edges())
        print(self.init_graph.edges())
        if (self.current_box_graph.edges() == self.init_graph.edges()):
            print("adj satisfied")
            return True
        else:
            print("adj not satisfied")
            return False

class App:
    def __init__(self) -> None:
        """
        @rahil.jain
        13/5/23
        """
        self.level = 8
        self.gameData()
        self.initialise_root()
        self.title_section()
        self.connectivity_graph_section()
        self.user_grid_section()
        self.inventory_section()
        self.buttons_section()

    def gameData(self):
        self.game_data = GameData(self.level)

    def connectivity_graph_section(self):
        self.connectivity_graph_frame = tk.Frame(self.root, width=self.screen_width/4, height=self.screen_height/2, highlightbackground="blue", highlightthickness=2)
        self.connectivity_graph_frame.grid(row=1, column=0)
        self.create_connectivity_graph()

    def clear_frame(self, frame):
        for widgets in frame.winfo_children():
            widgets.destroy()

    def create_connectivity_graph(self):
        title = tk.Canvas(self.connectivity_graph_frame, width=self.screen_width/4, height=self.screen_height/2)
        title.grid()
        title.create_text(100, 50, text="Connectivity", font=helv8)
        f = plt.Figure(figsize=(3, 3), dpi=100)
        ax = f.add_subplot(111)
        g = nx.Graph()
        g.add_edges_from(self.game_data.adjacency_list)
        # nx.draw(g, pos=nx.spectral_layout(g), ax=ax, with_labels=True, node_color="#ADD8E6")
        nx.draw(g, pos=nx.spring_layout(g), ax=ax, with_labels=True, node_color="#ADD8E6")
        # nx.draw_planar(g, ax=ax, with_labels=True, node_color="#ADD8E6")
        canvas = FigureCanvasTkAgg(f, self.connectivity_graph_frame)

        self.connectivity_graph_canvas = canvas.get_tk_widget()
        self.connectivity_graph_canvas.grid(row=0,column=0)
        print(self.connectivity_graph_canvas, "canv")



    def user_grid_section(self):
        
        self.user_grid_frame = tk.Frame(self.root, width=self.screen_width*0.7, height=self.screen_height/2, highlightbackground="blue", highlightthickness=2)
        self.user_grid_frame.grid(row=1, column=1)
        self.create_user_grid()

    def create_user_grid(self):
        title = tk.Label(self.user_grid_frame, text="User Grid", font=helv8)
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
                title.place(x = 100 + c*self.game_data.width_quanta , y = 100 + self.game_data.height_quanta*r)
        pass

    def drag_start(self, event, i):
        box = self.game_data.box_frames[i]
        # saving the start point of the box
        box.startX = event.x
        box.startY = event.y

    def drag_motion(self, event, i):
        box = self.game_data.box_frames[i]

        # finding the new location of the box
        ogX = box.winfo_x() - box.startX + event.x
        ogY = box.winfo_y() - box.startY + event.y
        x = min(max(ogX, 0), self.user_grid_frame.winfo_width() - box.winfo_width())
        y = min(max(ogY, 0), self.user_grid_frame.winfo_height() - box.winfo_height())
        print(x, y)
        print("start")
        # print(x, y)
        user_grid_frame_x = self.user_grid_frame.winfo_x()
        user_grid_frame_y = self.user_grid_frame.winfo_y()


        # Snapping Functionality
        if(x >= 100 and x <= 100 + 50 * (self.game_data.grid_col_size)
           and y >= 100 and y <= 100 + 50 * (self.game_data.grid_row_size)):
            x = ((x - 100) // self.game_data.width_quanta) * self.game_data.width_quanta + 100
            y = ((y - 100) // self.game_data.height_quanta) * self.game_data.height_quanta + 100 

        # x = ((x - 122 - user_grid_frame_x) // self.game_data.width_quanta) * self.game_data.width_quanta + 122 + user_grid_frame_x
        # y = ((y - 135 - user_grid_frame_y) // self.game_data.height_quanta) * self.game_data.height_quanta + 135 + user_grid_frame_y
        print(x, y)

        box.place(x = x, y = y)

        self.game_data.boxes_cur_x[i]=x
        self.game_data.boxes_cur_y[i]=y

    def rotate_box(self, i):
        print("rotating")
        box = self.game_data.box_frames[i]

        temp = self.game_data.box_sizes[i][0]
        self.game_data.box_sizes[i][0] = self.game_data.box_sizes[i][1]
        self.game_data.box_sizes[i][1] = temp

        
        print(box.winfo_width(), box.winfo_height())
        print(self.game_data.box_sizes[i])

        box.config(width =  box.winfo_height(), height=box.winfo_width())
    def inventory_section(self):
        title = tk.Label(self.user_grid_frame, text="Boxes", font=helv8)
        title.place(x = 500, y = 50)

        cur_x = 500
        cur_y = 100

        for i in range(len(self.game_data.box_sizes)):
            print(i, "index")
            self.game_data.box_frames[i] = tk.Frame(self.user_grid_frame, highlightthickness=2, width=self.game_data.width_quanta*self.game_data.box_sizes[i][0], height=self.game_data.height_quanta*self.game_data.box_sizes[i][1], bg=hex_colors[i])
            self.game_data.box_frames[i].place(x = cur_x, y = cur_y)
            box_num = tk.Label(self.game_data.box_frames[i], text=i, bg=hex_colors[i])
            box_num.place(relx=0.5, rely=0.5, anchor="center")
            self.game_data.box_frames[i].bind("<Button-1>", lambda event, i=i : self.drag_start(event, i))
            self.game_data.box_frames[i].bind("<B1-Motion>", lambda event, i=i : self.drag_motion(event, i))
            self.game_data.box_frames[i].bind("<Button-2>", lambda event, i=i : self.rotate_box(i))

            box_num.bind("<Button-1>", lambda event, i=i : self.drag_start(event, i))
            box_num.bind("<B1-Motion>", lambda event, i=i : self.drag_motion(event, i))
            box_num.bind("<Button-2>", lambda event, i=i : self.rotate_box(i))
            self.game_data.boxes_init_x[i]=cur_x
            self.game_data.boxes_init_y[i]=cur_y
            self.game_data.boxes_cur_x[i]=cur_x
            self.game_data.boxes_cur_y[i]=cur_y

            cur_x += 150
            if(cur_x > 800):
                cur_x = 500
                cur_y += 100
        
    def buttons_section(self):
        
        self.buttons_section_frame = tk.Frame(self.root, width=self.screen_width/2, height=self.screen_height/10, highlightbackground="blue", highlightthickness=2)
        self.buttons_section_frame.grid(row=2, column=0, columnspan=3)

        self.create_btn = tk.Button(self.buttons_section_frame, text="Create new")
        self.clear_btn = tk.Button(self.buttons_section_frame, text="Clear", command=lambda : self.reset())
        self.submit_btn = tk.Button(self.buttons_section_frame, text="Submit", command=lambda : self.game_data.check_game_success(self.output_text))
        self.next_level_btn = tk.Button(self.buttons_section_frame, text="Next Level", command=lambda : self.next_level(self.output_text))
        self.output_text = tk.Label(self.buttons_section_frame,text="Keep Going....")
        # self.create_btn.grid()

        self.submit_btn.grid()
        self.clear_btn.grid()
        self.next_level_btn.grid()
        self.output_text.grid()

    def next_level(self, label):
        self.level += 1
        if(self.level == 10):
            self.level = 1
        print("next level",self.level)
        self.game_data = GameData(self.level)
        self.refresh_ui()

    def refresh_ui(self):
        self.clear_frame(self.user_grid_frame)
        self.clear_frame(self.connectivity_graph_frame)
        self.inventory_section()
        self.create_connectivity_graph()
        self.create_user_grid()
        self.inventory_section()
        pass

    def reset(self):
        for i in range(0, len(self.game_data.box_frames)):
            print(i)
            box_frame = self.game_data.box_frames[i]
            box_frame.place(x = self.game_data.boxes_init_x[i], 
                            y = self.game_data.boxes_init_y[i])

    def run(self):
        self.root.mainloop()

    def initialise_root(self):
        self.root = tk.Tk()
        self.root.title("The Grid Game")
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(str(str(self.screen_width) +
                           'x' + str(self.screen_height)))

    def title_section(self):
        self.logo_frame = tk.Frame(self.root, highlightbackground="blue", highlightthickness=2)
        self.logo_frame.grid(row=0, column=0,columnspan=3)
        logo_canvas = tk.Canvas(self.logo_frame, width=self.screen_width*0.9, height=100)
        logo_canvas.pack()
        logo_canvas.create_text(200, 50, text="The Grid Game", font=helv15)


def run():
    app = App()
    app.run()


if __name__ == "__main__":
    app = App()
    app.run()

