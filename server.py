import socket, time
from core.constantes import IP, PORT
from network.servidornetwork import ServidorNetwork
from schema.basedatos import BaseDatos
from core.herramientas import Herramientas as her
from schema.querys import Querys



class Server():
    
    def __init__(self):
        info = her.cargar_json("data/ConfiguracionServidor.json")
        self.bd = BaseDatos(info.get("Mysql"))
        self.querys = Querys(self.bd)
        self.querys.registrar_usuario("admin", "12345")
        print("Registrado el usuario")
        time.sleep(5)
        self.socket = socket.socket()
        self.socket.bind((IP, PORT))
        self.socket.listen(0)
        
    def iniciar(self):
        print("[OK] Servidor Iniciado")
        while False:
            cliente, direccion = self.socket.accept()
            objeto_cliente = ServidorNetwork(cliente, direccion)
            print(f"Se intenta conectar: {direccion}")
            objeto_cliente.start()
            
            
if __name__ == "__main__":
    Server().iniciar()
            
