import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from constants import *

def create_bg_grid(app, row, col, frame):
    
    for r in range(row):
        for c in range(col):
            title = tk.Frame(app.user_grid_frame, highlightbackground="light grey", highlightthickness=1, width=50, height=50)
            title.place(x = 100 + c*app.game_data.width_quanta , y = 100 + app.game_data.height_quanta*r)
    pass

class UserGridSection:

    def create_user_grid(app):
        title = tk.Label(app.user_grid_frame, text="User Grid", font=helv8)
        title.place(x = 100, y = 50)
        create_bg_grid(app, app.game_data.grid_row_size, app.game_data.grid_col_size, app.user_grid_frame)

        # title = tk.Label(self.user_grid_frame, text="asdf")
        # title.place(x = 100 , y = 99)
        # self.user_grid_canvas = tk.Canvas(self.user_grid_frame, width=self.screen_width/3, height=self.screen_height/2)
        # self.user_grid_canvas.grid()
        # self.user_grid_canvas.create_text(50, 50, text="User Grid")

