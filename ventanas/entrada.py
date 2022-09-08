from ventanas.widgets_predefinidos import MDScreenAbstrac

class Entrada(MDScreenAbstrac):
    
    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.set_activo(True)
        
        
    def ingresar_usuario(self):
        pass
    
    def recuperar_contra(self):
        pass
        
    def actualizar(self, *dt):
        return super().actualizar(*dt)
    
    def siguiente(self, *dt):
        return super().siguiente(*dt)
    
    def volver(self, *dt):
        return super().volver(*dt)