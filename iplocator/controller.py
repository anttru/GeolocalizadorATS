from tkinter import Tk
from iplocator import model
from iplocator.view import View
from iplocator.model import Model

class Controller:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("1920x1080")
        self.root.title("Geolocalizador de IPs ATS")
        self.model = Model()
        self.view = View(self.root, self.model)
    def run(self):
        self.root.mainloop()