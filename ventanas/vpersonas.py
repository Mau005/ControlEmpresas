from ventanas.widgets_predefinidos import MDScreenAbstrac
from kivy.properties import ObjectProperty

class VPersonas(MDScreenAbstrac):
    botones = ObjectProperty()
    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.data = {
            'Crear': 'pencil',
            'Formatear': 'delete',
            'Salir': 'exit-run',
        }
        self.botones.data = self.data
        
    def accion_boton(self, args):
        print(args)