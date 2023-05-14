import tkinter as tk
import networkx as nx
import matplotlib
matplotlib.use("TkAgg")
import json
from collections import namedtuple

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
