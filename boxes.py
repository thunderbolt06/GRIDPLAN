import matplotlib
matplotlib.use("TkAgg")
from constants import *

class Box:
    def drag_start(app, event, i):
        box = app.game_data.box_frames[i]
        # saving the start point of the box
        box.startX = event.x
        box.startY = event.y

    def drag_motion(app, event, i):
        box = app.game_data.box_frames[i]

        # finding the new location of the box
        ogX = box.winfo_x() - box.startX + event.x
        ogY = box.winfo_y() - box.startY + event.y
        x = min(max(ogX, 0), app.user_grid_frame.winfo_width() - box.winfo_width())
        y = min(max(ogY, 0), app.user_grid_frame.winfo_height() - box.winfo_height())

        # Snapping Functionality
        if(x >= 100 and x <= 100 + 50 * (app.game_data.grid_col_size)
           and y >= 100 and y <= 100 + 50 * (app.game_data.grid_row_size)):
            x = ((x - 100) // app.game_data.width_quanta) * app.game_data.width_quanta + 100
            y = ((y - 100) // app.game_data.height_quanta) * app.game_data.height_quanta + 100 

        box.place(x = x, y = y)
        app.game_data.boxes_cur_x[i]=x
        app.game_data.boxes_cur_y[i]=y

    def rotate_box(app, i):
        print("rotating")
        box = app.game_data.box_frames[i]

        temp = app.game_data.box_sizes[i][0]
        app.game_data.box_sizes[i][0] = app.game_data.box_sizes[i][1]
        app.game_data.box_sizes[i][1] = temp
        box.config(width =  box.winfo_height(), height=box.winfo_width())