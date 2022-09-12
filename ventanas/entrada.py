from curses.ascii import controlnames
from ventanas.widgets_predefinidos import MDScreenAbstrac
from kivy.properties import ObjectProperty
from kivy.logger import Logger

from ventanas.widgets_predefinidos import Notificacion
from core.herramientas import Herramientas as her


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
        
    def guardado(self, correo, contraseña, boton):
        self.contenido_usuario["Usuario"]["contraseña"] = correo
        self.contenido_usuario["Usuario"]["correo"] = contraseña
        self.contenido_usuario["Usuario"]["boton"] = boton
        self.entrada_usuario = correo
        self.pass_usuario = contraseña

        her.escribir_json(self.contenido_usuario, "data/ConfiguracionCliente.json")
        
    def ingresar_usuario(self, correo, password):
        if self.ids.usuario_guardar.active:
            if not(self.contenido_usuario["Usuario"]["contraseña"] == self.pass_usuario.text):
                self.guardado(her.cifrado_sha1(self.pass_usuario.text),self.entrada_usuario.text, self.ids.usuario_guardar.active)
            else:
                self.pass_usuario.text = her.cifrado_sha1(self.pass_usuario.text)
        else:
            self.guardado("", "", False)
            self.pass_usuario.text = her.cifrado_sha1(self.pass_usuario.text)
        
        if len(correo) >= 2 and len(password) >= 2:
            estructura = {"estado":"login", "correo":correo, "password":password}
            self.network.enviar(estructura)
            info = self.network.recibir()
            if info.get("estado"):
                
                Logger.info("Usuario Iniciado de forma exitosa")
                noti = Notificacion(f"Querido: {correo}", "Se ha iniciado seccion con exito")
                self.siguiente()
                noti.open()
            else:
                noti = Notificacion("Error", "Usuario o Contraseña invalida")
                noti.open()
        else:
            noti = Notificacion("Error", "Tiene que ser mas de 2 caracteres en usaurio o password")
            noti.open()
    
    def recuperar_contra(self):
        pass
        
    def actualizar(self, *dt):
        return super().actualizar(*dt)
    
    def siguiente(self, *dt):
        return super().siguiente(*dt)
    
    def volver(self, *dt):
        return super().volver(*dt)