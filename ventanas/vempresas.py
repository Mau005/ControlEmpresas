from ventanas.widgets_predefinidos import MDScreenAbstrac, Notificacion
from kivymd.uix.pickers import MDDatePicker
from kivy.properties import ObjectProperty
import datetime
from entidades.registroservicio import RegistroServicios
from core.constantes import BUTTONCREATE

class VEmpresas(MDScreenAbstrac):
        
    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.set_activo(True)
        self.data = BUTTONCREATE
        self.ids.botones.data = self.data
        self.correo = "prueba"
        
        
        
    def accion_boton(self, arg):
        print(arg)
        if arg.icon == "exit-run":
            self.siguiente()
        
    def actualizar(self, *dt):
        return super().actualizar(*dt)
    
    def siguiente(self, *dt):
        return super().siguiente(*dt)
    
    def volver(self, *dt):
        return super().volver(*dt)
        
    