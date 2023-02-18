import socket
import sys

from network.servidornetwork import ServidorNetwork
from schema.basedatos import BaseDatos
from core.herramientas import Herramientas as her
from schema.querys import Querys
from network.control_network import Control_Network
import threading, time
from servicios_correos.servicio_correos import Servicio_Correos

MOTD = """
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
        try:
            self.socket = socket.socket()
            self.socket.bind((self.info["Servidor"]["ip"], self.info["Servidor"]["port"]))
            self.socket.listen(5)
        except OSError as error:
            print(error)
            input("Precione para continuar")
            sys.exit()

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
    print(sys.argv)

    if len(sys.argv) >= 2:
        if sys.argv[1] == "setup":
            iniciando = True
    if iniciando:
        print(MOTD)
        while True:
            info = her.cargar_json("data/ConfiguracionServidor.json")
            bd = BaseDatos(info.get("Mysql"))
            querys = Querys(bd)
            import getpass

            try:
                contra = getpass.getpass(prompt="[PREPARANDO] Indicame la contraseña para el usuario admin: ")
                contra2 = getpass.getpass(prompt="[PREPARANDO] Indicame nuevamente la contraseña: ")
                if len(contra) >= 3 and contra == contra2:
                    from entidades.registroempresas import RegistroEmpresas
                    from entidades.cuentas import Cuentas
                    from entidades.personas import Personas

                    rut_base = "11.111.111-1"
                    base_string = "Persona Natural"
                    empresa = querys.registrar_empresas(RegistroEmpresas(rut_empresa=rut_base,
                                                                         nombre_empresa=base_string,
                                                                         giro_empresa=base_string,
                                                                         direccion_empresa=base_string,
                                                                         telefono_empresa="",
                                                                         correo_empresa=base_string,
                                                                         correo_respaldo="",
                                                                         celular_empresa=""))
                    base_string_admin = "Admin User"
                    persona = querys.registrar_persona_sin_cuenta(Personas(rut_persona=rut_base,
                                                                  nombres=base_string_admin,
                                                                  apellidos=base_string_admin,
                                                                  celular=base_string_admin,
                                                                  correo=base_string_admin,
                                                                  rut_empresa=rut_base))
                    cuenta = querys.registrar_cuenta(Cuentas(rut_persona=rut_base,
                                                    nombre_cuenta="admin",
                                                    contraseña=contra,
                                                    acceso=5
                                                    ))
                    print(f"Cuenta: {cuenta}")
                    print("[OK] Usuario admin registrado con exito")
            except Exception as err:
                print('ERROR:', err)

            print("[PREPARANDO] Registrando tablas minimas para funcionar")

            querys.registrar_estados("OPERATIVO")
            querys.registrar_estados("DETENIDO")
            querys.registrar_estados("PENDIENTE")
            querys.registrar_estados("COMPLETADO")
            querys.registrar_estados("MASTER")

            querys.registrar_estado_gastos("COMUNES")
            querys.registrar_estado_gastos("REMUNERACIONES")
            querys.registrar_estado_gastos("TRANSPORTES")
            querys.registrar_estado_gastos("INSUMOS")
            querys.registrar_estado_gastos("ARRIENDO")
            querys.registrar_estado_gastos("COMBUSTIBLES")
            querys.registrar_estado_gastos("INMUEBLES")
            querys.registrar_estado_gastos("SIN BOLETAS/SIN DOCUMENTOS")
            querys.registrar_estado_gastos("OTROS")
            print("[OK] Se han registrado todos los atributos necesarios")
            break
    else:
        servidor = Server()
        servidor.iniciar()
