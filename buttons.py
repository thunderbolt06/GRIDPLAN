import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from constants import *

class Button:
    def create_buttons(app):
        app.buttons_section_frame = tk.Frame(app.root, width=app.screen_width/2, height=app.screen_height/10, highlightbackground="blue", highlightthickness=2)
        app.buttons_section_frame.grid(row=2, column=0, columnspan=3)

        app.create_btn = tk.Button(app.buttons_section_frame, text="Create new")
        app.clear_btn = tk.Button(app.buttons_section_frame, text="Reset", command=lambda : app.reset())
        app.submit_btn = tk.Button(app.buttons_section_frame, text="Submit", command=lambda : app.game_data.check_game_success(app.output_text))
        app.next_level_btn = tk.Button(app.buttons_section_frame, text="Next Level", command=lambda : app.next_level(app.output_text))
        app.output_text = tk.Label(app.buttons_section_frame,text="Keep Going....")

        app.submit_btn.grid()
        app.clear_btn.grid()
        app.next_level_btn.grid()
        app.output_text.grid()
