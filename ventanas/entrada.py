from curses.ascii import controlnames
from ventanas.widgets_predefinidos import MDScreenAbstrac
from kivy.properties import ObjectProperty
from kivy.logger import Logger

from ventanas.widgets_predefinidos import Notificacion
from core.herramientas import Herramientas as her
from core.constantes import PROTOCOLOERROR


class Entrada(MDScreenAbstrac):
    entrada_usuario = ObjectProperty()
    pass_usuario = ObjectProperty()
    
    
    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.set_activo(True)
        self.contenido_usuario = her.cargar_json("data/ConfiguracionCliente.json")
        Logger.info("Se Cargado la configuración")
        
        if self.contenido_usuario["Usuario"]["boton"]:
            self.entrada_usuario.text = self.contenido_usuario["Usuario"]["correo"]
            self.pass_usuario.text = self.contenido_usuario["Usuario"]["contraseña"]
            
        self.ids.usuario_guardar.active = self.contenido_usuario["Usuario"]["boton"]
        
    def guardado(self, correo, contraseña, boton, condicion = False):
        self.contenido_usuario["Usuario"]["contraseña"] = contraseña
        self.contenido_usuario["Usuario"]["correo"] = correo
        self.contenido_usuario["Usuario"]["boton"] = boton
        if condicion:
            self.entrada_usuario.text = correo
            self.pass_usuario.text = contraseña

        her.escribir_json(self.contenido_usuario, "data/ConfiguracionCliente.json")
        
    def ingresar_usuario(self, correo, password):
        if self.ids.usuario_guardar.active:
            if not(self.contenido_usuario["Usuario"]["contraseña"] == password):
                password = her.cifrado_sha1(password)
                self.guardado(self.entrada_usuario.text, password, self.ids.usuario_guardar.active)
                
        else:
            self.guardado("", "", False, condicion = True)
            password = her.cifrado_sha1(password)
            
        
        if len(correo) >= 2 and len(password) >= 2:
            estructura = {"estado":"login", "correo":correo, "password":password}
            self.network.enviar(estructura)
            info = self.network.recibir()
            if info.get("estado"):
                noti = Notificacion(f"Querido: {correo}", info.get("MOTD"))
                self.siguiente()
                noti.open()
            else:
                condicion = info.get("condicion")
                if condicion == "NETWORK":
                    noti = Notificacion("Error", PROTOCOLOERROR[info.get("condicion")] + " Desea intentar conectarse Nuevamente? ", funcion_concurrente=self.network.iniciar)
                    noti.open()
                
        else:
            noti = Notificacion("ror", "Tiene que ser mas de 2 caracteres en usaurio o passwordEr")
            noti.open()
    
    def recuperar_contra(self):
        pass
        
    def actualizar(self, *dt):
        return super().actualizar(*dt)
    
    def siguiente(self, *dt):
        return super().siguiente(*dt)
    
    def volver(self, *dt):
        return super().volver(*dt)