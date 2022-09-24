from ventanas.widgets_predefinidos import MDScreenAbstrac
from kivy.properties import ObjectProperty
import sys

class Casa(MDScreenAbstrac):
    lista_productos = ObjectProperty()

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)

    def crear_servicios(self):
        self.manager.current = "servicios"

    def crear_usuarios(self):
        self.manager.current = "personas"

    def cambiar_ventanta(self, ventana):
        self.manager.get_screen(ventana).activar()
        self.manager.current = ventana

    def salir(self, *Arg):
        self.volver()
        self.network.enviar({"estado":"desconectar"})


    def actualizar(self, *dt):
        return super().actualizar(*dt)

    def siguiente(self, *dt):
        return super().siguiente(*dt)

    def volver(self, *dt):
        return super().volver(*dt)
