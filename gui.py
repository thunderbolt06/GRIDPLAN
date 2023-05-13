import tkinter as tk


helv15 = ("Helvetica", 15, "bold")
helv8 = ("Helvetica", 8, "bold")
colors = [
    "#7B68EE",  # medium slate blue
    "#40E0D0",  # turqouise
    "#FF7F50",  # coral
    "#FF69B4",  # hot pink
    "#E6E6FA",  # lavender
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
    "#E6E6FA",  # lavender
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
        self.adjacency_graph = [(1,2), (2,3), (3,1)]
        self.rfp = None



class App:
    def __init__(self) -> None:
        self.initialise_root()
        self.title_section()
        self.connectivity_graph_section()
        self.user_grid_section()
        self.inventory_section()
        self.buttons_section()

    def connectivity_graph_section(self):
        self.connectivity_graph_frame = tk.Frame(self.root, width=self.screen_width/4, height=self.screen_height/2, highlightbackground="blue", highlightthickness=2)
        self.connectivity_graph_frame.grid(row=1, column=0)

        title = tk.Canvas(self.connectivity_graph_frame, width=self.screen_width/4, height=self.screen_height/2)
        title.grid()
        title.create_text(50, 50, text="Connectivity")

    def user_grid_section(self):
        
        self.user_grid_frame = tk.Frame(self.root, width=self.screen_width*0.7, height=self.screen_height/2, highlightbackground="blue", highlightthickness=2)
        self.user_grid_frame.grid(row=1, column=1)
        
        self.create_bg_grid(5, 4, self.user_grid_frame)

        # title = tk.Label(self.user_grid_frame, text="asdf")
        # title.place(x = 100 , y = 99)
        # self.user_grid_canvas = tk.Canvas(self.user_grid_frame, width=self.screen_width/3, height=self.screen_height/2)
        # self.user_grid_canvas.grid()
        # self.user_grid_canvas.create_text(50, 50, text="User Grid")

    def create_bg_grid(self, row, col, frame):
        
        for r in range(row):
            for c in range(col):
                title = tk.Frame(self.user_grid_frame, highlightbackground="light grey", highlightthickness=2, width=50, height=50)
                title.place(x = 100 + c*50 , y = 100 + 50*r)
        pass

    def inventory_section(self):
        pass
        # self.inventory_frame = tk.Frame(self.root, width=self.screen_width/3, height=self.screen_height, highlightbackground="blue", highlightthickness=2)
        # self.inventory_frame.grid(row=1, column=2)
        # self.inventory_canvas = tk.Canvas(self.inventory_frame, width=self.screen_width/3, height=self.screen_height/2)
        # self.inventory_canvas.grid()
        # self.inventory_canvas.create_text(50, 50, text="Boxes")

        # self.boxes = {}
        # rect = self.inventory_frame(50, 110,300,280, fill= "light blue")
        # label = tk.Label(self.root, bg="red", width=10, height=5)
        # label.place(x=0, y=0)
        # self.boxes[rect] = {}
        # self.inventory_canvas.tag_bind(rect, "<Button-1>", lambda event : self.drag_start(event, rect, self.inventory_canvas))
        # # self.inventory_canvas.tag_bind(rect, "<Button-1>", lambda x: print("hello"))
        # self.inventory_canvas.tag_bind(rect, "<B1-Motion>", lambda event : self.drag_motion(event, rect, self.inventory_canvas))
        # self.inventory_canvas.bind("<B1-Motion>", lambda event : self.drag_motion(event, rect))





    def drag_start(self, event, rect, canvas):
        print(rect)
        print(canvas.coords(rect))
        self.boxes[rect]["startX"] = event.x
        self.boxes[rect]["startY"] = event.y
        # rect.startX = event.x
        # rect.startY = event.y

    def drag_motion(self, event, rect, canvas):
        # x = rect.winfo_x() - rect.startX + event.X
        # y = rect.winfo_Y() - rect.startY + event.y
        # rect.place(x=x, y=y)
        pass

        
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

