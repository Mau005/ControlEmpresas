

class RegistroNotas:
    def __init__(self,**kargs):
        self.id_registro = kargs.get("id_registro")
        self.nota = kargs.get("nota")
        self.fecha_creacion = kargs.get("fecha_creacion")
        self.rut_asociado = kargs.get("rut_asociado")
        self.rut_persona = kargs.get("rut_persona")
        self.nombre_creado = kargs.get("nombre_creado")
        
    def preparar(self, registro) -> dict:
        return {"estado":registro, "contenido":self}
    
    def __str__(self) -> str:
        return '''
    ID Registro: {}
    nota: {}
    Fecha Creacion {}
    Rut Asociado: {}
    rut_persona: {}
    Nombre Creado: {}
    '''.format(self.id_registro, self.nota, self.fecha_creacion, self.rut_asociado, self.rut_persona, self.nombre_creado)
    
