
from ventanas.widgets_predefinidos import MDScreenAbstrac

class Servicios(MDScreenAbstrac):
        
    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.set_activo(True)
        
        self.estructura = {
            "ID_Servicio": None,
            "Nombre": None,
            "Descr": None,
            "Fecha_Inicio": None,
            "Fecha_Termino": None,
            "Historial_Registros": None,
            "Correo": None,
            "Estado": None,
        }
        
    def actualizar(self, *dt):
        return super().actualizar(*dt)
    
    def siguiente(self, *dt):
        return super().siguiente(*dt)
    
    def volver(self, *dt):
        return super().volver(*dt)
        
    