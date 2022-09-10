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
        
    def ingresar_usuario(self, usuario, password):
        print(f"usuario: {usuario} Password: {password}")
        noti = Notificacion("Hola", "mama esta presa",funcion_concurrente=self.func_new)
        noti.open()
        if len(usuario) >= 2 and len(password) >= 2:
            pass
        else:
            pass
    
    def recuperar_contra(self):
        pass
        
    def actualizar(self, *dt):
        return super().actualizar(*dt)
    
    def siguiente(self, *dt):
        return super().siguiente(*dt)
    
    def volver(self, *dt):
        return super().volver(*dt)