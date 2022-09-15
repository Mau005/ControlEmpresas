import socket
from core.constantes import IP, PORT
from network.servidornetwork import ServidorNetwork
from schema.basedatos import BaseDatos
from core.herramientas import Herramientas as her
from schema.querys import Querys



class Server():
    #Kastachaña: ordenar separar en idioma aymara
    
    def __init__(self):
        self.info = her.cargar_json("data/ConfiguracionServidor.json")
        self.grupos = her.cargar_json("data/Grupos.json")["Grupos"]
        self.bd = BaseDatos(self.info.get("Mysql"))
        self.querys = Querys(self.bd)
        self.socket = socket.socket()
        self.socket.bind((IP, PORT))
        self.socket.listen(0)
        
    def iniciar(self):
        print("[OK] Servidor Iniciado")
        while True:
            cliente, direccion = self.socket.accept()
            objeto_cliente = ServidorNetwork(cliente, direccion,self.querys, self.info, self.grupos)
            print(f"Se intenta conectar: {direccion}")
            objeto_cliente.start()
            
            
if __name__ == "__main__":
    Server().iniciar()
            
