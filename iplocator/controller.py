import tkinter
from iplocator.view import View
from iplocator.model import Model
import platform

class Controller:
    #Esta clase crea la vista y el controlador y los relaciona
    def __init__(self):
        #creo una ventana de tkinter a pantalla completa, tamaño no cambiable y con un título
        self.root = tkinter.Tk()
        if platform.system() == "Windows":
            self.root.state("zoomed")
        else:
            self.root.attributes("-zoomed", True)
        self.root.resizable(False, False)
        self.root.title("Geolocalizador de IPs ATS")

        #obtengo el ancho y el alto
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.root.geometry("{}x{}".format(width, height))

        #creo el modelo y la vista y los comunico        
        self.model = Model(self.root)
        self.view = View(self.root, self.model, width, height)
        self.model.view = self.view
    
    def run(self):
        self.root.mainloop()