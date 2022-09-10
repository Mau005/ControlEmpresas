from threading import Thread
from core.constantes import TAMANIO_PAQUETE
from core.herramientas import Herramientas as her


class ServidorNetwork(Thread):
    
    def __init__(self, cliente, direccion, querys):
        Thread.__init__(self)
        self.cliente = cliente
        self.direccion = direccion
        self.querys = querys
        self.intentos = 0
        
    def enviar(self, datos):
        return self.cliente.send(her.empaquetar(datos))
    
    def recibir(self):
        datos = self.cliente.recv(TAMANIO_PAQUETE)
        
        if datos != b'':
            return her.desenpaquetar(datos)
        return {"estado": "cierreAbrupto"}
        
        
    def run(self):
        while True:
            datos = self.recibir()
            print(datos)
            if datos.get("estado") == "saludo":
                self.saludo()
                
            if datos.get("estado") == "login":
                self.login(datos)
                
            if datos.get("estado") == "registroservicio":
                pass
                
            elif datos.get("estado") == "cierreAbrupto":
                print("Cliente se ha desconectado de forma anormal, por que nos abe que el ctm tiene que colocar salir seccion")
                break
            
    def login(self, datos):
        correo = datos.get("correo")
        passw = datos.get("password")
        datosnuevos = self.querys.consultar_usuario(correo,passw)
        if datosnuevos.get("estado"):
            self.intentos = 0
        else:
            self.intentos += 1
            
        if self.intentos >= 3:
            self.enviar({"estado": False, "condicion": "Intentos completados procedaras a ser baneado FDP"})
            self.cliente.close()
            print(f"Intentos: {self.intentos}")
            
        self.enviar(datosnuevos)
        
    def saludo(self):
        self.enviar({"estado": "saludo", "contenido": "Hola fdp del servidor"})