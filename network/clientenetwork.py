from core.constantes import TAMANIO_PAQUETE, CONFIGURATION_WARNING
from core.herramientas import Herramientas as her
from kivy.logger import Logger
import socket


class ClienteNetwork:

    def __init__(self):
        self.socket = None
        self.__estado = False
        self.configuracion = self.cargar_json()
        self.ip = self.configuracion["Servidor"]["ip"]
        self.port = self.configuracion["Servidor"]["port"]
        self.iniciar()

    def cargar_json(self, actualizar=False):
        configuracion = her.cargar_json("data/ConfiguracionCliente.json")
        if configuracion is None:
            return CONFIGURATION_WARNING

        if actualizar:
            configuracion["Servidor"]["ip"] = self.ip
            configuracion["Servidor"]["port"] = self.port
            her.escribir_json(configuracion, "data/ConfiguracionCliente.json")
        return configuracion

    def iniciar(self, *args):
        try:
            self.socket = socket.socket()
            self.socket.settimeout(2)
            self.socket.connect((self.ip, self.port))
            self.socket.settimeout(None)
            self.configuracion = self.cargar_json(actualizar=True)
            self.__estado = True
            Logger.info("Se ha conectado con exito")
            return self.socket
        except socket.error as error:
            Logger.critical("Problemas para conectarse hacia el servidor")
            self.__estado = False

    def enviar(self, datos):
        if self.__estado:
            try:
                self.socket.send(her.empaquetar(datos))
            except BrokenPipeError as error:
                Logger.critical("Caida abrupta del sistema")
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
