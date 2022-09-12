

class RegistroEmpresas():
    
    def __init__(self, **kargs):
        self.rut_empresa = kargs.get("rut_empresa")
        self.nombre_empresa = kargs.get("nombre_embresa")
        self.giro = kargs.get("giro_empresa")
        self.direccion = kargs.get("direccion_emSpresa")
        self.telefono = kargs.get("telefono")
        self.correo1 = kargs.get("correo1")
        self.correo2 = kargs.get("correo2")
        self.celular = kargs.get("celular")
        
    def preparar(self):
        return {"estado": "registroempresa", "contenido":self}
        
        