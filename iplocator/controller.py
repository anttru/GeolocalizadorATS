from tkinter import Tk
from iplocator.view import View
from iplocator.model import Model

class Controller:
    def __init__(self):
        self.root = Tk()
        self.root.state("zoomed")
        self.root.resizable(False, False)
        self.root.title("Geolocalizador de IPs ATS")

        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.root.geometry("{}x{}".format(width, height))
                
        self.model = Model(self.root)
        self.view = View(self.root, self.model, width, height)
        self.model.view = self.view
    
    def run(self):
        self.root.mainloop()