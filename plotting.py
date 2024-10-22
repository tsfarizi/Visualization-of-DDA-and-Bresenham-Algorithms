import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class PlotCanvas:
    """Class to handle plotting on a Matplotlib canvas within Tkinter."""
    def __init__(self, parent_frame, title):

        self.figure, self.ax = plt.subplots(figsize=(6, 6), dpi=100)
        self.ax.set_title(title, fontsize=14)
        
        self.setup_axes(-50, 50, -50, 50)

        self.draw_grid()
        self.draw_axes()

        self.canvas = FigureCanvasTkAgg(self.figure, master=parent_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().config(width=600, height=600)
        self.canvas.get_tk_widget().pack(side='top')

        self.toolbar = NavigationToolbar2Tk(self.canvas, parent_frame)
        self.toolbar.update()
        self.toolbar.pack(side='top')

        self.title = title

    def clear(self):
        self.ax.cla()  
        self.setup_axes(-50, 50, -50, 50)  
        self.draw_grid()
        self.draw_axes()

    def setup_axes(self, x_min, x_max, y_min, y_max):
        self.ax.set_xlim(x_min, x_max)
        self.ax.set_ylim(y_min, y_max)
        self.ax.set_aspect('equal', adjustable='box')

        major_tick = 10
        minor_tick = 5

        self.ax.set_xticks(np.arange(x_min, x_max+1, major_tick))
        self.ax.set_yticks(np.arange(y_min, y_max+1, major_tick))
        self.ax.set_xticks(np.arange(x_min, x_max+1, minor_tick), minor=True)
        self.ax.set_yticks(np.arange(y_min, y_max+1, minor_tick), minor=True)

        self.ax.tick_params(axis='both', which='major', labelsize=7)
        self.ax.tick_params(axis='both', which='minor', labelsize=0)
        self.ax.grid(False)

    def draw_grid(self):
        self.ax.grid(which='minor', color='lightgray', linewidth=0.5)

    def draw_axes(self):
        self.ax.axhline(0, color='black', linewidth=2)
        self.ax.axvline(0, color='black', linewidth=2)

    def draw_line(self, x_values, y_values):
        self.ax.plot(x_values, y_values, color='black')

    def add_rectangle(self, x, y, color):
        rect = plt.Rectangle((x, y), 1, 1, facecolor=color, edgecolor='none')
        self.ax.add_patch(rect)

    def set_title(self):
        self.ax.set_title(self.title, fontsize=14)

    def refresh(self):
        self.canvas.draw()
