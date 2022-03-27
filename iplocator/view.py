from logging import root
import tkinter
from tkintermapview import TkinterMapView

class View:
    def __init__(self, root, model):
        self.root = root
        self.buttonsframe = tkinter.Frame(root, width= 320, height = 1080)
        self.mapframe = tkinter.Frame(root, width= 1600, height = 1080)
        map_widget = TkinterMapView(self.mapframe, width=1600, height=1080, corner_radius=0)
        map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.buttonsframe.place(x= 1600, y = 0)
        self.mapframe.place(x= 0, y = 0)
        #self.buttonsframe.pack(side=tkinter.RIGHT, fill=tkinter.Y, expand=1)
        self.plotBut = tkinter.Button(self.buttonsframe, text="Plot")
        self.plotBut.pack(side="top", fill=tkinter.BOTH)