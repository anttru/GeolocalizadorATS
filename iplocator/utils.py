from os import getpid
from random import choices
from struct import pack
from threading import Lock

#Este modulo contiene funciones de calculo de valores. Provienen de la libreria icmplib donde son funciones de clase. Contienen alguna modificiación menor, como la corrección de un error en calculatecheksum

def create_packet(id, sequence):
    #Monta los bits del paquete a partir de los campos
    checksum = 0 #El checksum se pone a 0 a efectos de su calculo
    payload = bytes(choices(b'abcdefghijklmnopqrstuvwxyz' b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'b'1234567890', k=56)) #Se genera un payload aleatorio de 56 bytes, el tamaño minimo
            
    header = pack('!2B3H', 8, 0, checksum, id, sequence) # La cabecera de 8 bytes, 2 unsigned char (B) seguido de 3 unsigned short (H)
    checksum = calculatechecksum(header + payload) #Se calcula el checksum tomando este como 0
    header = pack('!2B3H', 8, 0, checksum, id, sequence) #Se monta la cabecera con el checksum obtenido
    return header + payload

def calculatechecksum(data):
    #Esta funcion calcula el checksum del paquete.
    sum = 0
    data += b'\x00' #empieza iniciandolo a 0 en binario
    #De http://www.faqs.org/rfcs/rfc1071.html, se suman los bytes como palabras, luego se suma el carryout  
    for i in range(0, len(data) - 1, 2):
        sum += (data[i] << 8) + data[i + 1]
        sum  = (sum & 0xffff) + (sum >> 16) #las palabras tienen 16 bytes así que lo que de esta manera obtiene el overflow

    sum += (sum >>16) #Corrijo un error de la libreria original, que no contaba con posibilidad de segundo carryout tras el último, se recomienda hacerlo al final
    sum = ~sum & 0xffff #El calculo del checksum finaliza haciendo el complemento a 1 del resultado

    return sum


PID = getpid()
_lock_id = Lock()
_current_id = PID

def unique_identifier():
    #Esta funcion genera un identificador único entre 1 y 65535, el primero es 1 + el id de proceso
    global _current_id
    with _lock_id: #Usa un lock para restringir el acceso y que no sea escrito por varios a la vez
        _current_id += 1
        _current_id &= 0xffff #el &= asegura que retorne un valor unsigned int y no un negativo.
        return _current_id