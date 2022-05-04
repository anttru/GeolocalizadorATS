import tkinter
from tkinter import W, StringVar, ttk
from tkinter.messagebox import showinfo
from tkintermapview import TkinterMapView
from iplocator import FONT, SMALLERFONT
from iplocator.model import Model

class View:
    def __init__(self, root : tkinter.Tk, model: Model, width, height):
        self.root = root
        self.model = model
        self.marker = None
        self.pathcoordslist = []
        self.path = None
        self.width = width
        self.height = height
        self.data = {}
        self.valuestoip = {}

        self.buttonsframe = tkinter.Frame(root, width = width/4, height = height)
        self.mapframe = tkinter.Frame(root, width = width * 3/4, height = height)
        
        self.map_widget = TkinterMapView(self.mapframe, width = width * 3/4, height = height, corner_radius = 0)
        self.map_widget.place(relx = 0.5, rely = 0.5, anchor=tkinter.CENTER)
        self.map_widget.set_zoom(0)

        self.buttonsframe.place(x= width*3/4, y = 0)
        self.mapframe.place(x = 0, y = 0)

        self.labelIp = tkinter.Label(self.buttonsframe, text = "Escriba la IP objetivo:", font =FONT)
        #self.labelIp.pack(ipadx=20, ipady=20)
        self.labelIp.grid(column= 0, row= 0, sticky= tkinter.W, columnspan=2,padx= 20, pady = 20)

        self.targetIp = tkinter.StringVar()
        self.ipentry = tkinter.Entry(self.buttonsframe, textvariable=self.targetIp, font = FONT, width = 25)
        #self.ipentry.pack(fill = "x")
        self.ipentry.grid(column=0, row= 1, sticky=tkinter.W, columnspan=2, padx= 10)
        
        self.sendButton = tkinter.Button(self.buttonsframe, text = "Localizar", font = FONT, command = self.placeroute)
        #self.sendButton.pack(side = "left")
        self.sendButton.grid(column=0, row=2, sticky= tkinter.W, pady= 10, padx = 5)

        self.button = tkinter.Button(self.buttonsframe, text = "Borrar Todo", font = FONT, command = self.deletemarkers)
        #self.button.pack(side = "right")
        self.button.grid(column=1, row= 2, pady= 10, padx = 5)
        
        self.progressbar = ttk.Progressbar(self.buttonsframe, orient='horizontal', mode='determinate', length= width//8, maximum=30, value= 0)
        self.progressbar.grid(column=0, row = 3, columnspan= 2, sticky= tkinter.W)

        self.progresslabel = ttk.Label(self.buttonsframe, text = "Esperando entrada de IP")
        self.progresslabel.grid(column=0, row= 4, columnspan=2)

        self.dropdownmenu = ttk.Combobox( self.buttonsframe, state = "readonly", width = 50)
        self.dropdownmenu.bind("<<ComboboxSelected>>", self.showinfo)
        self.dropdownmenu.grid(column = 0, row = 5, columnspan=2, sticky= tkinter.W)
        self.createresultsform()
        self.hideform()
        
    def createresultsform(self):
        #Esta funcion contiene la creación y posicionamiento del formulario en el que se muestra la información de cada IP        
        #Creo las variables de texto que contendran la información
        self.countrytext = tkinter.StringVar(self.buttonsframe)
        self.regiontext = tkinter.StringVar(self.buttonsframe)
        self.citytext = tkinter.StringVar(self.buttonsframe)
        self.ziptext = tkinter.StringVar(self.buttonsframe)
        self.coordstext = tkinter.StringVar(self.buttonsframe)
        self.timezonetext = tkinter.StringVar(self.buttonsframe)
        self.isptext = tkinter.StringVar(self.buttonsframe)
        self.orgtext = tkinter.StringVar(self.buttonsframe)
        self.astext = tkinter.StringVar(self.buttonsframe)
        #Creo etiquetas para cada campo
        self.countrylabel = ttk.Label(self.buttonsframe, text = "País: ")
        self.regionlabel = tkinter.Label(self.buttonsframe, text = "Región: ")
        self.citylabel = tkinter.Label(self.buttonsframe, text = "Ciudad: ")
        self.ziplabel = tkinter.Label(self.buttonsframe, text = "Cod. Postal: ")
        self.coordslabel = tkinter.Label(self.buttonsframe, text = "Coordenadas: ")
        self.timezonelabel = tkinter.Label(self.buttonsframe, text = "Zona horaria: ")
        self.isplabel = tkinter.Label(self.buttonsframe, text = "ISP: ")
        self.orglabel = tkinter.Label(self.buttonsframe, text = "Organización")
        self.aslabel = tkinter.Label(self.buttonsframe, text = "as: ")
        #La información estará dentro de un cuadro de entrada no editable       
        self.countryentry = ttk.Entry(self.buttonsframe, font = SMALLERFONT, state="readonly", textvariable= self.countrytext, width = 35)
        self.regionentry = ttk.Entry(self.buttonsframe, font = SMALLERFONT, state="readonly", textvariable= self.regiontext, width = 35)
        self.cityentry = ttk.Entry(self.buttonsframe, font = SMALLERFONT, state="readonly", textvariable= self.citytext, width = 35)
        self.zipentry = ttk.Entry(self.buttonsframe, font = SMALLERFONT, state="readonly", textvariable= self.ziptext, width = 35)
        self.coordsentry = ttk.Entry(self.buttonsframe, font = SMALLERFONT, state="readonly", textvariable= self.coordstext, width = 35)
        self.timezoneentry = ttk.Entry(self.buttonsframe, font = SMALLERFONT, state="readonly", textvariable= self.timezonetext, width = 35)
        self.ispentry = ttk.Entry(self.buttonsframe, font = SMALLERFONT, state="readonly", textvariable= self.isptext, width = 35)
        self.orgentry = ttk.Entry(self.buttonsframe, font = SMALLERFONT, state="readonly", textvariable= self.orgtext, width = 35)
        self.asentry = ttk.Entry(self.buttonsframe, font = SMALLERFONT, state="readonly", textvariable= self.astext, width = 35)
        #Coloco los elementos creados anteriormente        
        self.countrylabel.grid(column=0, row= 6)
        self.regionlabel.grid(column=0, row= 7)
        self.citylabel.grid(column=0, row= 8)
        self.ziplabel.grid(column=0, row= 9)
        self.coordslabel.grid(column=0, row= 10)
        self.timezonelabel.grid(column=0, row= 11)
        self.isplabel.grid(column=0, row= 12)
        self.orglabel.grid(column=0, row= 13)
        self.aslabel.grid(column=0, row= 14)
        
        self.countryentry.grid(column= 1, row = 6)
        self.regionentry.grid(column= 1, row = 7)
        self.cityentry.grid(column= 1, row = 8)
        self.zipentry.grid(column= 1, row = 9)
        self.coordsentry.grid(column= 1, row = 10)
        self.timezoneentry.grid(column= 1, row = 11)
        self.ispentry.grid(column= 1, row = 12)
        self.orgentry.grid(column= 1, row = 13)
        self.asentry.grid(column= 1, row = 14)
        #Los escondo, luego con hacer .grid() sin parámetros recordarán su posición        
        self.hideform()

    def hideform(self):
        #esta función hace que los elementos del formulario de presentación desaparezcan
        self.countrylabel.grid_remove()
        self.regionlabel.grid_remove()
        self.citylabel.grid_remove()
        self.ziplabel.grid_remove()
        self.coordslabel.grid_remove()
        self.timezonelabel.grid_remove()
        self.isplabel.grid_remove()
        self.orglabel.grid_remove()
        self.aslabel.grid_remove()
        
        self.countryentry.grid_remove()
        self.regionentry.grid_remove()
        self.cityentry.grid_remove()
        self.zipentry.grid_remove()
        self.coordsentry.grid_remove()
        self.timezoneentry.grid_remove()
        self.ispentry.grid_remove()
        self.orgentry.grid_remove()
        self.asentry.grid_remove()

        self.dropdownmenu.grid_remove()
    
    def showform(self):
        #grid() sin parámetros recuerda la última configuración grid que tuvieron, esta función mostrará los elementos del formulario si estan ocultos.
        self.countrylabel.grid()
        self.regionlabel.grid()
        self.citylabel.grid()
        self.ziplabel.grid()
        self.coordslabel.grid()
        self.timezonelabel.grid()
        self.isplabel.grid()
        self.orglabel.grid()
        self.aslabel.grid()
        
        self.countryentry.grid()
        self.regionentry.grid()
        self.cityentry.grid()
        self.zipentry.grid()
        self.coordsentry.grid()
        self.timezoneentry.grid()
        self.ispentry.grid()
        self.orgentry.grid()
        self.asentry.grid()

    def showinfo(self,a):
        ip = self.valuestoips[self.dropdownmenu.get()]
        self.map_widget.delete(self.marker)
        self.marker = None
        if ip == None:
            self.hideform()
            self.dropdownmenu.grid()
            self.map_widget.set_zoom(0)
        else:
            self.showform()
            if self.data[ip]["status"] == "success":
                self.marker = self.map_widget.set_marker(self.data[ip]["lat"] ,self.data[ip]["lon"], text=ip)
                self.map_widget.set_zoom(5)
                self.map_widget.set_position(self.data[ip]["lat"] ,self.data[ip]["lon"])
                self.countrytext.set("{} ({})".format(self.data[ip]["country"],self.data[ip]["countryCode"]))
                self.regiontext.set("{} ({})".format(self.data[ip]["regionName"],self.data[ip]["region"]))
                self.citytext.set("{}".format(self.data[ip]["city"]))
                self.ziptext.set("{}".format(self.data[ip]["zip"]))
                self.coordstext.set("{},{}".format(self.data[ip]["lat"],self.data[ip]["lon"]))
                self.timezonetext.set("{}".format(self.data[ip]["timezone"]))
                self.isptext.set("{}".format(self.data[ip]["isp"]))
                self.orgtext.set("{}".format(self.data[ip]["org"]))
                self.astext.set("{}".format(self.data[ip]["as"]))
            else:
                self.countrytext.set("IP Privada")
                self.countrytext.set("IP Privada")
                self.regiontext.set("IP Privada")
                self.citytext.set("IP Privada")
                self.ziptext.set("IP Privada")
                self.coordstext.set("IP Privada")
                self.timezonetext.set("IP Privada")
                self.isptext.set("IP Privada")
                self.orgtext.set("IP Privada")
                self.astext.set("IP Privada")

    def placeLocation(self):
        ipdata = self.model.getIpData(self.targetIp.get())
        self.markersList.append(self.map_widget.set_marker(ipdata["lat"], ipdata["lon"], text = self.targetIp.get()))

    def deletemarkers(self):
        self.pathcoordslist = []
        if self.path != None:
            self.map_widget.delete(self.path)
            self.path.delete()
        self.path =  None
        self.progressbar["value"] = 0
        self.progressbar["maximum"] = 30
        self.progresslabel["text"] = "Esperando entrada de IP"
        self.model.ipdata = []
        self.model.iplist = []
        self.dropdownmenu["values"] = []
        self.data = {}
        self.valuestoips = {}
        self.hideform()
        self.dropdownmenu.set("")
        if self.marker != None:
            self.map_widget.delete(self.marker)
            self.marker = None
        self.map_widget.set_zoom(0)

    def createdropdownvalues(self, iplist):
        values = ["Seleccione un router para ver su información"]
        counter = 1
        self.valuestoips = {"Seleccione un router para ver su información": None}
        for ip in iplist:
            values.append("Router {} : {}".format(counter, ip))
            self.valuestoips["Router {} : {}".format(counter, ip)] = ip
            counter += 1
        return values

    def placeroute(self):
        self.deletemarkers()
        try:
            self.model.getiplist(self.targetIp.get())
            self.model.getipdata()
        except Exception as e :
            self.progresslabel["text"] =  e
                    
        self.markersList = []
        for ip in self.model.ipdata:
            self.root.update()
            if ip["status"] == "success":
                #self.markersList.append(self.map_widget.set_marker(ip["lat"], ip["lon"], text = ip["query"]))
                self.pathcoordslist.append((ip["lat"], ip["lon"]))
        if len(self.pathcoordslist) > 0:
            self.path = self.map_widget.set_path(self.pathcoordslist)
        self.data = dict(zip(self.model.iplist, self.model.ipdata))
        self.dropdownmenu.grid()
        self.dropdownmenu["values"] = self.createdropdownvalues(self.model.iplist)
        self.dropdownmenu.current(0)