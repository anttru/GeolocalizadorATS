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
    def __init__(self):
        self.targetIp = ""
        self.iplist = []
        self.ipdata = []
        
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
            raise SyntaxError("Invalid URL")
        try :
            ip = IP(ip)
        except: 
            raise SyntaxError("Invalid IP")
        if ip.version() != 4:
            raise SyntaxError("Only IPv4s are accepted")
        
        p = subprocess.Popen(["tracert", ip.strFullsize()], stdout=subprocess.PIPE)
        while True:
            line = p.stdout.readline()
            if not line:
                break
            lines.append(str(line))

        pattern = re.compile(IP_REGEX)       
        for line in lines:
            if pattern.search(line):
                self.iplist.append(pattern.search(line)[0])
        if len(self.iplist) > 1:
            self.iplist.pop(0)

        return self.iplist

    def getroutedata(self):
        self.ipdata = []
        for ip in self.iplist:
            self.ipdata.append(self.getIpData(ip))
        return self.ipdata