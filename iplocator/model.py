from tkinter import Tk
import requests
from iplocator import API_URL, IP_REGEX
import subprocess
import re
from IPy import IP
from socket import gethostbyname

class APIError(Exception):
    pass
class SyntaxError(Exception):
    pass

class Model:
    def __init__(self, root : Tk, view = None):
        self.targetIp = ""
        self.root = root
        self.iplist = []
        self.ipdata = []
        self.view = view
        
    def getIpData(self, ip):
        ipdata = requests.get(API_URL.format(ip))
        if ipdata.status_code != 200:
            raise APIError("failed to retrieve ip geolocation data from API")
        return ipdata.json()

    
    def getiplist(self, iporurl):
        lines = []
        self.iplist = []
        try:
            ip = gethostbyname(iporurl)
        except:
            raise SyntaxError("URL no encontrada")
        try :
            ipobject = IP(ip)
        except: 
            raise SyntaxError("No es una IP válida")
        if ipobject.version() != 4:
            raise SyntaxError("Sólo se aceptan IPv4s")
        if ipobject.iptype() != "PUBLIC":
            raise SyntaxError("Solo se aceptan IPs de rango público")
        
        p = subprocess.Popen(["tracert", "-w", "150", "-d", ip], stdout=subprocess.PIPE)
        while True:
            self.root.update()
            line = p.stdout.readline()
            if not line:
                break
            lines.append(str(line))
            self.view.progressbar["value"] += 1
            self.view.progresslabel["text"] = "Hop {} de un máximo de 30".format(self.view.progressbar["value"] - 3)

        pattern = re.compile(IP_REGEX)       
        for line in lines:
            if pattern.search(line):
                self.iplist.append(pattern.search(line)[0])
        if len(self.iplist) > 1:
            self.iplist.pop(0)
        return self.iplist

    def getipdata(self):
        self.ipdata = []
        self.view.progressbar["maximum"] = len(self.iplist)
        self.view.progressbar["value"] = 0
        for ip in self.iplist:
            self.root.update()    
            self.ipdata.append(self.getIpData(ip))
            self.view.progressbar["value"] += 1
            self.view.progresslabel["text"] = "Obteniendo datos de IPs {} de {}".format( self.view.progressbar["value"], len(self.iplist))
        self.view.progresslabel["text"] = "Completado con éxito"
        return self.ipdata