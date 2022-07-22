from core.constantes import IP, PORT, TAMANIO_PAQUETE
from core.herramientas import Herramientas as her

import socket

class ClienteNetwork():
    
    def __init__(self):
        self.socket = None
        self.__estado = False
        self.__iniciar()
        
        
    def __iniciar(self):
        try:
            self.socket = socket.socket()
            self.socket.connect((IP, PORT))
            self.__estado = True
            print("SE HA CONECTADO CON EXITO FDP")
            return self.socket
        except socket.error as error:
            print(error)
            self.__estado = False
            
    def enviar(self, datos):
        if self.__estado:
            self.socket.send(her.empaquetar(datos))
            
        
    def recibir(self):
        return her.desenpaquetar(self.socket.recv(TAMANIO_PAQUETE))
            
            
    def consultar_estado(self):
        return self.__estado
    
    def conectar_network(self):
        self.__iniciar()
        return self.__estado
            
    def cerrar(self):
        if self.__estado:
            self.socket.close()
            print("Cerrado con Exito")
        