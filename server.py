import socket
from core.constantes import IP, PORT
from network.servidornetwork import ServidorNetwork
from schema.basedatos import BaseDatos
from core.herramientas import Herramientas as her
from schema.querys import Querys
from network.control_network import Control_Network
import threading, time


class Server:
    # Kastachaña: ordenar separar en idioma aymara

    def __init__(self):
        self.tiempo_ejecucion = None
        self.__tiempos()
        self.enfuncionamiento = True
        self.__iniciar_variables()
        self.__configurar_servidor()
        self.__tiempos()
        tiempo = threading.Thread(target=self.actualizar)
        tiempo.start()

    def __tiempos(self):
        self.tiempo_inicial = time.time()

    def __iniciar_variables(self):
        self.info = her.cargar_json("data/ConfiguracionServidor.json")
        self.grupos = her.cargar_json("data/Grupos.json")["Grupos"]
        self.bd = BaseDatos(self.info.get("Mysql"))
        self.querys = Querys(self.bd)
        self.control_network = Control_Network()

    def __configurar_servidor(self):
        self.socket = socket.socket()
        self.socket.bind((IP, PORT))
        self.socket.listen(0)

    def actualizar(self):
        while self.enfuncionamiento:
            tiempo_transcurrido = time.time()
            time.sleep(2)
            self.tiempo_ejecucion = tiempo_transcurrido - self.tiempo_inicial
        # self.control_network.actualizar()

    def iniciar(self):

        print("[OK] Servidor Iniciado")
        while self.enfuncionamiento:
            cliente, direccion = self.socket.accept()
            objeto_cliente = ServidorNetwork(cliente, direccion, self.querys, self.info, self.grupos,
                                             self.control_network)
            print(f"Se intenta conectar: {direccion}")
            objeto_cliente.start()
        self.enfuncionamiento = False


if __name__ == "__main__":
    Server().iniciar()
