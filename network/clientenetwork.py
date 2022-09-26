from core.constantes import PORT, TAMANIO_PAQUETE
from core.herramientas import Herramientas as her
from kivy.logger import Logger
from ventanas.widgets_predefinidos import Notificacion
import socket


class ClienteNetwork:

    def __init__(self):
        self.socket = None
        self.__estado = False
        self.ip = "localhost"
        self.iniciar()

    def iniciar(self, *args):
        try:
            self.socket = socket.socket()
            self.socket.settimeout(10)
            self.socket.connect((self.ip, PORT))
            self.socket.settimeout(None)
            self.__estado = True
            Logger.info("Se ha conectado con exito")
            return self.socket
        except socket.error as error:
            Logger.critical("Problemas para conectarse hacia el servidor")
            self.__estado = False
            noti = Notificacion("Error de conexión",
                                " Aun no se ha podido establecer la conexión al servidor, intententelo mas tarde")
            noti.open()

    def enviar(self, datos):
        if self.__estado:
            try:
                self.socket.send(her.empaquetar(datos))
            except BrokenPipeError as error:
                print(f"Caida abrupta del sistema")
        return {"estado": False, "condicion": "NETWORK"}

    def recibir(self):
        if self.__estado:
            return her.desenpaquetar(self.socket.recv(TAMANIO_PAQUETE))
        return {"estado": False, "condicion": "NETWORK"}

    def consultar_estado(self):
        return self.__estado

    def conectar_network(self):
        self.iniciar()
        return self.__estado

    def cerrar(self):
        if self.__estado:
            self.socket.close()
            print("Cerrado con Exito")
