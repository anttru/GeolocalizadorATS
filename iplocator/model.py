import platform
from tkinter import Tk
import requests
from iplocator import API_URL, IP_REGEX
import subprocess
import re
from IPy import IP
from socket import gethostbyname
from time import sleep, time
import socket
from iplocator.utils import calculatechecksum, unique_identifier, create_packet

class APIError(Exception):
    pass
class SyntaxError(Exception):
    pass
class ConnectionError(Exception):
    pass
class TimeoutException(Exception):
    pass

class Model:
    #Esta clase hará la parte de negocio, obtendra las IPs del camino y obtendrá sus datos de la API
    #Creo las estructuras de datos que contendran la lista de IPs obtenidas y sus datos
    def __init__(self, root : Tk, view = None):
        self.targetIp = ""
        self.root = root
        self.iplist = []
        self.ipdata = []
        self.notreachedflag = False #Indica si el tracert no llego a la IP objetivo
        self.view = view

    #Esta función obtiene los datos de una IP de la API usando requests, si no se obtiene respuesta lanza excepción
    def getIpData(self, ip):
        ipdata = requests.get(API_URL.format(ip))
        if ipdata.status_code != 200:
            raise APIError("failed to retrieve ip geolocation data from API")
        return ipdata.json()

    def validateiporurl(self, iporurl):
        #Se resuelve la url a una IP por DNS, si es una IP, nos devuelve la misma IP, si no existe, lanzamos excepción
        try:
            ip = gethostbyname(iporurl)
        except:
            raise SyntaxError("URL o IP no válida")
        #La clase IP de IPy da una excepción si se crea con una IP no válida
        #también tiene métodos para sacar información sobre la IP, con ellos valido que la IP es valida, v4 y pública
        try :
            ipobject = IP(ip)
        except: 
            raise SyntaxError("No es una IP válida")
        if ipobject.version() != 4:
            raise SyntaxError("Sólo se aceptan IPv4s")
        if ipobject.iptype() != "PUBLIC":
            raise SyntaxError("Solo se aceptan IPs de rango público")
        return ip

    #Esta función obtiene las IPs haciendo un tracert a la ip objetivo y actualiza la barra de progreso
    def getiplist(self, iporurl):
        self.iplist = []
        ip = self.validateiporurl(iporurl)
        #Lanzamos un subproceso  tracert con Popen.
        if platform.system() == "Windows":
            self.getipsWin(ip)
        else:
            self.traceroute(ip)
        return ip #retornamos la ip objetivo para poder usarla en la vista

    def getipsWin(self, ip):
        #Lanzamos un subproceso  tracert con Popen.
        lines = []
        tracertprocess = subprocess.Popen(["tracert", "-w", "500", "-d", ip], stdout=subprocess.PIPE)
        while True:
            self.root.update() #se actualiza la pantalla para que no se cuelgue tkinter al interrumpir el mainloop con el while
            line = tracertprocess.stdout.readline() #recuperamos las líneas que genera tracert
            if not line:
                break
            lines.append(str(line))
            if ip != None and self.view != None: #Las interacciones con View se limitan al caso de que exista para poder usar este módulo independientemente.
                self.view.progressbar["value"] += 1  #actualizamos el valor de la barra de progreso
                self.view.progresslabel["text"] = "Hop {} de un máximo de 30".format(self.view.progressbar["value"] - 3)
        self.iplist = self.extractIPs(lines) #extraemos las ips del texto del tracert
        if self.iplist[-1] != ip: #Si no se ha llegado al objetivo, se añade pero se activa un flag para informar del error
            self.iplist.append(ip)
            self.notreachedflag = True
    
    def traceroute(self, ip, maxhops = 30):
        #Implementación de traceroute, haciendo uso de la funcion ttlicmpecho(), retorna una lista de ips
        routers = []
        for ttl in range(1,maxhops+1):
            router = None
            router = self.ttlicmpecho(ip, ttl = ttl)
            if router:
                self.iplist.append(router)
            if router == ip:
                break
        return routers
    
    def ttlicmpecho(self, ip, count = 3, interval = 0.5, timeout = 0.6, ttl = 30):
        #Esta función manda peticiones de echo individuales con un ttl dado, buscando que responda un hop intermedio, la usare para implementar mi propio traceroute
        icmpsocket =  socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_RAW,
            proto=socket.IPPROTO_ICMP)
        #Se crea una socket raw, que administramos desde la programación en vez del kernel
        replies = []
        id = unique_identifier() #se crea el idenfiticador
        
        for sequence in range(count):
            sleep(interval) # Para no enviar todas las peticiones de golpe esperamos medio segundo entre paquetes

        try:
            send(ip,id, sequence, icmpsocket, ttl)
            reply = None
            reply = receive(timeout, icmpsocket) #receive retornará directamente la ip del router que responde
            
        except Exception as e:
            print(e)

        replies.append(reply)
        #Hemos hecho varios intentos, miramos si alguno ha respondido y si lo ha hecho, retornamos esa ip como resultado
        for reply in replies:
            if reply:
                return reply

    def extractIPs(self, lines):
        #esta función extrae IPs a partir de una expresión regular de una lista de líneas de texto    
        iplist = []
        pattern = re.compile(IP_REGEX)       
        for line in lines:
            if pattern.search(line):
                iplist.append(pattern.search(line)[0])
        if len(iplist) > 1:
            iplist.pop(0) #la primera línea contiene la ip objetivo, que ya aparece en la última línea.
        return iplist

    #Obtenemos los datos de todas las IPs y los guardamos en una lista, actualiza la barra de progreso
    def getipdatalist(self):
        self.ipdata = []
        if self.view != None:
            self.view.progressbar["maximum"] = len(self.iplist)
            self.view.progressbar["value"] = 0
        for ip in self.iplist:
            self.root.update()    #Se actualiza la pantalla para que no se cuelgue tkinter
            self.ipdata.append(self.getIpData(ip))
            if self.view != None: 
                self.view.progressbar["value"] += 1
                self.view.progresslabel["text"] = "Obteniendo datos de IPs {} de {}".format( self.view.progressbar["value"], len(self.iplist))
        if self.view != None:
            self.view.progresslabel["text"] = "Completado con éxito"
        return self.ipdata
    
def send(ip, id, sequence, icmpsocket : socket.socket, ttl):
    #esta función envía desde una socket con un tll, ip objetivo e id especificadas como argumentos
    packet = create_packet(id, sequence) #montamos el paquete a envíar
    icmpsocket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL,ttl) #Se configura el ttl en la socket
    target = socket.getaddrinfo(ip, port=None, family= icmpsocket.family, type=icmpsocket.type)[0][4] #Se obtiene el objetivo en formato necesario para la socket
    icmpsocket.sendto(packet, target)

def receive(timeout, icmpsocket : socket.socket):
    #esta funcion recibe en una socket dada con un timeout dado
    icmpsocket.settimeout(timeout)
    time_limit = time() + timeout #calculo del tiempo límite para recibir respuesta
    try:
        while True:
            response = icmpsocket.recvfrom(1024)
            current_time = time()
            source = None
            source = response[1][0] #Se obtiene el remitente de la respuesta obtenida

            if current_time > time_limit:
                raise socket.timeout
            return source
    
    except socket.timeout:
        raise TimeoutException("Tiempo de espera superado ({}s)".format(timeout))
    except OSError:
        raise OSError