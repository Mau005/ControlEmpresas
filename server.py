import socket
from network.servidornetwork import ServidorNetwork
from schema.basedatos import BaseDatos
from core.herramientas import Herramientas as her
from schema.querys import Querys
from network.control_network import Control_Network
import threading, time
from servicios_correos.servicio_correos import Servicio_Correos

MOTD= """
 ____  __.                __                .__                          
|    |/ _|____    _______/  |______    ____ |  |__ _____    ____ _____   
|      < \__  \  /  ___/\   __\__  \ _/ ___\|  |  \ \__  \  /    \ \__  \  
|    |  \ / __ \_\___ \  |  |  / __ \ \  \___|   Y  \/ __ \|   |  \/ __ \_
|____|__ (____  /____  > |__| (____  /\___  >___|  (____  /___|  (____  /
        \/    \/     \/            \/     \/     \/     \/     \/     \/ 
Creado por Mau
https://github.com/Mau005
"""

class Server:
    # Kastachaña: ordenar separar en idioma aymara

    def __init__(self):
        self.tiempo_ejecucion = 0
        self.__tiempos()
        self.enfuncionamiento = True
        self.__iniciar_variables()
        self.__configurar_servidor()
        self.__tiempos()
        self.tiempo = threading.Thread(target=self.actualizar)
        self.tiempo.start()

    def __tiempos(self):
        self.tiempo_inicial = time.time()

    def __iniciar_variables(self):
        print(MOTD)
        self.info = her.cargar_json("data/ConfiguracionServidor.json")
        print("[OK] Se Cargan Variables")
        self.grupos = her.cargar_json("data/Grupos.json")["Grupos"]
        print("[OK] Se cargan los Grupos")
        self.servicio_correos = Servicio_Correos(self.info["Correo"]["correo"],
                                                 self.info["Correo"]["contraseña"],
                                                 self.info["Correo"]["host"],
                                                 self.info["Correo"]["port"])
        print("[OK] Se cargan Información del correo electronico no-reply")

        self.bd = BaseDatos(self.info.get("Mysql"))
        self.querys = Querys(self.bd)
        self.control_network = Control_Network()

    def __configurar_servidor(self):
        self.socket = socket.socket()
        self.socket.bind((self.info["Servidor"]["ip"], self.info["Servidor"]["port"]))
        self.socket.listen(0)

    def actualizar(self):
        while self.enfuncionamiento:
            self.tiempo_ejecucion += 1
            self.control_network.actualizar()
            time.sleep(1)

    def cerrar(self):
        self.enfuncionamiento = False
        self.tiempo.join()

    def iniciar(self):
        print("[OK] Servidor Iniciado: {}:{}".format(self.info["Servidor"]["ip"], self.info["Servidor"]["port"]))
        while self.enfuncionamiento:
            cliente, direccion = self.socket.accept()
            objeto_cliente = ServidorNetwork(cliente, direccion, self.querys, self.info, self.grupos,
                                             self.control_network, self.servicio_correos)
            print(f"Se ha conectado: {direccion}")
            objeto_cliente.start()
        self.cerrar()


if __name__ == "__main__":
    iniciando = False
    if iniciando:
        print(MOTD)
        while True:
            info = her.cargar_json("data/ConfiguracionServidor.json")
            bd = BaseDatos(info.get("Mysql"))
            querys = Querys(bd)
            print("Sistema de registro del administrador... ")

            import getpass
            try:
                print("Indicame la contraseña para el administrador: ")
                contra = getpass.getpass()
                print("Indicame nuevamente la contraseña: ")
                contra2 = getpass.getpass()
                if len(contra) >= 3 and contra == contra2:
                    querys.registrar_cuenta("admin", contra)
                    break
            except Exception as err:
                print('ERROR:', err)


    else:
        servidor = Server()
        servidor.iniciar()

