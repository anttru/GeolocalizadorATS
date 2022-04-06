from importlib.resources import path
import tkinter
from tkintermapview import TkinterMapView
from iplocator import FONT
from iplocator.model import Model

class View:
    def __init__(self, root, model: Model, width, height):
        self.root = root
        self.model = model
        self.markersList = []
        self.pathiplist = []
        self.path = None
        self.width = width
        self.height = height

        self.buttonsframe = tkinter.Frame(root, width = width/4, height = height)
        self.mapframe = tkinter.Frame(root, width = width * 3/4, height = height)
        
        self.map_widget = TkinterMapView(self.mapframe, width = width * 3/4, height = height, corner_radius = 0)
        self.map_widget.place(relx = 0.5, rely = 0.5, anchor=tkinter.CENTER)
        self.map_widget.set_zoom(0)

        self.buttonsframe.place(x= width*3/4, y = 0)
        self.mapframe.place(x = 0, y = 0)

        self.labelIp = tkinter.Label(self.buttonsframe, text = "Escriba la IP objetivo", font =FONT)
        self.labelIp.pack(ipadx=20, ipady=20)

        self.targetIp = tkinter.StringVar()
        self.ipentry = tkinter.Entry(self.buttonsframe, textvariable=self.targetIp, font = FONT)
        self.ipentry.pack(fill = "x")

        self.sendButton = tkinter.Button(self.buttonsframe, text = "Localizar", font = FONT, command = self.placeroute)
        self.sendButton.pack(side = "left")
        
        self.button = tkinter.Button(self.buttonsframe, text = "Borrar Todo", font = FONT, command = self.deletemarkers)
        self.button.pack(side = "right")
        
            
    def placeLocation(self):
        ipdata = self.model.getIpData(self.targetIp.get())
        self.markersList.append(self.map_widget.set_marker(ipdata["lat"], ipdata["lon"], text = self.targetIp.get()))

    def deletemarkers(self):
        for marker in self.markersList:
            marker.delete()
        self.markersList = []
        self.pathiplist = []
        self.path.delete()
        self.path =  None
        self.map_widget = TkinterMapView(self.mapframe, width = self.width * 3/4, height = self.height, corner_radius = 0)
        self.map_widget.place(relx = 0.5, rely = 0.5, anchor=tkinter.CENTER)
        self.map_widget.set_zoom(0)
    
    def addToPath(self, coordinates):
        if self.path == None:
            self.path = self.map_widget.set_path([(52.57, 13.4), (52.55, 13.35)])
    
    def placeroute(self):
        self.model.getiplist(self.targetIp.get())
        self.model.getroutedata()
        self.markersList = []
        for ip in self.model.ipdata:
            if ip["status"] == "success":
                self.markersList.append(self.map_widget.set_marker(ip["lat"], ip["lon"], text = ip["query"]))
                self.pathiplist.append((ip["lat"], ip["lon"]))
        self.path = self.map_widget.set_path(self.pathiplist)