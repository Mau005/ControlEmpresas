from ventanas.widgets_predefinidos import MDScreenAbstrac
from kivy.properties import ObjectProperty

from ventanas.widgets_predefinidos import Notificacion


class Entrada(MDScreenAbstrac):
    entrada_usuario = ObjectProperty()
    pass_usuario = ObjectProperty()
    
    
    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.set_activo(True)
        
    def func_new(self, *args):
        print("soy la nueva funcion")
        
    def ingresar_usuario(self, correo, password):
        print(f"usuario: {correo} Password: {password}")

        if len(correo) >= 2 and len(password) >= 2:
            estructura = {"estado":"login", "correo":correo, "password":password}
            self.network.enviar(estructura)
            info = self.network.recibir()
            print(f"El estado que me enviaron es: {info}")
            if info.get("estado"):
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