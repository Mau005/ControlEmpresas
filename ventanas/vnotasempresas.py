from ventanas.widgets_predefinidos import MDScreenAbstrac
from core.constantes import BUTTONCREATE

class VNotasEmpresas(MDScreenAbstrac):
    
    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.ids.botones.data = BUTTONCREATE
    
    
    def accion_boton(self, arg):
        
        if arg.icon == "pencil":
            print("Pintar")
            
        if arg.icon == "delete":
            self.formatear()
        
        if arg.icon == "exit-run":
            self.siguiente()
            
    def formatear(self):
        pass
    
    def siguiente(self, *dt):
        return super().siguiente(*dt)
    
    def volver(self, *dt):
        return super().volver(*dt)
    
    def actualizar(self, *dt):
        return super().actualizar(*dt)