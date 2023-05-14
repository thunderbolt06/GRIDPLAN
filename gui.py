import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from gameData import GameData
from connectivityGraph import ConnectivityGraph
from userGridSection import UserGridSection
from buttons import Button
from boxes import Box
from constants import *

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

    def buttons_section(self):
        Button.create_buttons(self)

    def user_grid_section(self):
        self.user_grid_frame = tk.Frame(self.root, width=self.screen_width*0.7, height=self.screen_height/2, highlightbackground="blue", highlightthickness=2)
        self.user_grid_frame.grid(row=1, column=1)
        UserGridSection.create_user_grid(self)

    def gameData(self):
        self.game_data = GameData(self.level)

    def connectivity_graph_section(self):
        self.connectivity_graph_frame = tk.Frame(self.root, width=self.screen_width/4, height=self.screen_height/2, highlightbackground="blue", highlightthickness=2)
        self.connectivity_graph_frame.grid(row=1, column=0)
        ConnectivityGraph.create_connectivity_graph(self)

    def clear_frame(self, frame):
        for widgets in frame.winfo_children():
            widgets.destroy()

    def inventory_section(self):
        title = tk.Label(self.user_grid_frame, text="Boxes", font=helv8)
        title.place(x = 500, y = 50)

        cur_x = 500
        cur_y = 100

        for i in range(len(self.game_data.box_sizes)):
            self.game_data.box_frames[i] = tk.Frame(self.user_grid_frame, highlightthickness=2, width=self.game_data.width_quanta*self.game_data.box_sizes[i][0], height=self.game_data.height_quanta*self.game_data.box_sizes[i][1], bg=hex_colors[i])
            self.game_data.box_frames[i].place(x = cur_x, y = cur_y)
            box_num = tk.Label(self.game_data.box_frames[i], text=i, bg=hex_colors[i])
            box_num.place(relx=0.5, rely=0.5, anchor="center")
            self.game_data.box_frames[i].bind("<Button-1>", lambda event, i=i : Box.drag_start(self, event, i))
            self.game_data.box_frames[i].bind("<B1-Motion>", lambda event, i=i : Box.drag_motion(self, event, i))
            self.game_data.box_frames[i].bind("<Button-2>", lambda event, i=i : Box.rotate_box(self, i))

            box_num.bind("<Button-1>", lambda event, i=i : Box.drag_start(self, event, i))
            box_num.bind("<B1-Motion>", lambda event, i=i : Box.drag_motion(self, event, i))
            box_num.bind("<Button-2>", lambda event, i=i : Box.rotate_box(self, i))
            self.game_data.boxes_init_x[i]=cur_x
            self.game_data.boxes_init_y[i]=cur_y
            self.game_data.boxes_cur_x[i]=cur_x
            self.game_data.boxes_cur_y[i]=cur_y

            cur_x += 150
            if(cur_x > 800):
                cur_x = 500
                cur_y += 100
        
    def next_level(self, label):
        self.level += 1
        if(self.level == 10):
            self.level = 1
        print("next level",self.level)
        self.game_data = GameData(self.level)
        self.refresh_ui()
        self.level_option = f"level {self.level}"
        self.logo_canvas.itemconfig(self.level_title, text=f"Level {self.level}")
        # self.level_title.config
        # self.level_dropdown.config()

    def refresh_ui(self):
        self.clear_frame(self.user_grid_frame)
        self.clear_frame(self.connectivity_graph_frame)
        ConnectivityGraph.create_connectivity_graph(self)
        UserGridSection.create_user_grid(self)
        self.inventory_section()

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
        logo_canvas = tk.Canvas(self.logo_frame, width=self.screen_width*0.6, height=100)
        logo_canvas.grid(row=0, column=0)
        # logo_canvas.place(x = 50, y = 50)
        logo_canvas.create_text(200, 50, text="The Grid Game", font=helv15)
        self.logo_canvas = logo_canvas
        self.level_title = logo_canvas.create_text(500, 50 , text=f"Level {self.level}", font=helv15)
        # self.level_option = tk.StringVar()
        # self.level_option.set("level 1")
        # self.level_dropdown = tk.OptionMenu( self.logo_frame , self.level_option , *options, command=lambda level_option = self.level_option: self.choose_level(level_option))
        # # self.level_dropdown.place(x = 700, y = 50)
        # self.level_dropdown.grid(row=0, column=1, padx = 100)


    def choose_level(self, level_option):
        self.level = int(level_option[6:])
        self.refresh_ui()


def run():
    app = App()
    app.run()

if __name__ == "__main__":
    app = App()
    app.run()

