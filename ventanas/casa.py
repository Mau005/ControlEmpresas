from ventanas.widgets_predefinidos import MDScreenAbstrac
from kivy.properties import ObjectProperty

class Casa(MDScreenAbstrac):
    
    lista_productos = ObjectProperty()
    
    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        
    def actualizar(self, *dt):
        return super().actualizar(*dt)
    
    def siguiente(self, *dt):
        return super().siguiente(*dt)
    
    def volver(self, *dt):
        return super().volver(*dt)