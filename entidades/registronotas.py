

class RegistroNotas:
    def __init__(self,**kargs):
        self.id_registro = kargs.get("id_registro")
        self.nota = kargs.get("nota")
        self.fecha_creacion = kargs.get("fecha_creacion")
        self.rut_asociado = kargs.get("rut_asociado")
        self.id_cuenta = kargs.get("id_cuenta")
        
    def preparar(self, registro):
        return {"estado":registro, "contenido":self}
    
    def __str__(self):
        return '''
    ID Registro: {}
    nota: {}
    Fecha Creacion {}
    Rut Asociado: {}
    ID Cuenta: {}
    '''.format(self.id_registro, self.nota, self.fecha_creacion, self.rut_asociado, self.id_cuenta)
    
