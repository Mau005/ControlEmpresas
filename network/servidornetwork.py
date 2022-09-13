from threading import Thread
from core.constantes import TAMANIO_PAQUETE
from core.herramientas import Herramientas as her

from entidades.registroempresas import RegistroEmpresas
from entidades.registrousaurios import RegistroUsuarios


class ServidorNetwork(Thread):
    
    def __init__(self, cliente, direccion, querys, info):
        Thread.__init__(self)
        self.cliente = cliente
        self.direccion = direccion
        self.querys = querys
        self.intentos = 0
        self.info = info
        self.usuario = RegistroUsuarios()
        
        
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
            if datos.get("estado") == "saludo":
                self.saludo()
                
            if datos.get("estado") == "login":
                self.login(datos)
                
            if datos.get("estado") == "registroservicio":
                self.registroservicios(datos)
                
            if datos.get("estado") == "registroempresa":
                self.registroempresas(datos.get("contenido"))
                
            if datos.get("estado") == "registro_notas_empresas":
                self.registronotasempresas(datos.get("contenido"))
                
            if datos.get("estado") == "listaEmpresas":
                self.listaEmpresas()
                
            if datos.get("estado") == "listadoservicios":
                self.listadoservicios()
                
            elif datos.get("estado") == "cierreAbrupto":
                print("Cliente se ha desconectado de forma anormal, por que nos abe que el ctm tiene que colocar salir seccion")
                break
            
    def listadoservicios(self):
        datos = self.querys.solicitar_listado_servicios()
        self.enviar(datos)
        
    def listaEmpresas(self):
        datos = self.querys.solicitar_lista_empresas()
        self.enviar(datos)
        
    def registronotasempresas(self, notas):      
        self.querys.registrar_notas_empresas(notas.notas ,notas.rut_empresa, self.usuario.correo,)
        
    def login(self, datos):
        correo = datos.get("correo")
        passw = datos.get("password")
        datosnuevos = self.querys.consultar_usuario(correo,passw)
        datosnuevos.update({"MOTD":self.info["Servidor"]["MOTD"]})
        if datosnuevos.get("estado"):
            self.intentos = 0
        else:
            self.intentos += 1
            
        if self.intentos >= 3:
            self.enviar({"estado": False, "condicion": "Intentos completados procedaras a ser baneado FDP"})
            self.cliente.close()
            print(f"Intentos: {self.intentos}")
        
        self.usuario = RegistroUsuarios(correo = datosnuevos["datos"][0], contraseña = datosnuevos["datos"][1],
                                        fecha_creacion = datosnuevos["datos"][1], estado_usuario = datosnuevos["datos"][2])
        self.enviar(datosnuevos)
        
    def registroservicios(self,datos):
        estado = self.querys.registrar_servicios(datos)
        self.enviar(estado)
        
    def registroempresas(self, empresa):
        objeto = RegistroEmpresas()
        objeto = empresa
        estado = self.querys.registrar_empresas(objeto)
        self.enviar(estado)
        
    def saludo(self):
        self.enviar({"estado": "saludo", "contenido": "Hola fdp del servidor"})