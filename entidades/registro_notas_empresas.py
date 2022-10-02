

class Registro_Notas_Empresas:
    def __init__(self,**kargs):
        self.id_registro = kargs.get("id_registro")
        self.notas = kargs.get("notas")
        self.rut_empresa = kargs.get("rut_empresa")
        self.correo = kargs.get("correo")
        self.fecha_creacion = kargs.get("fecha_creacion")
        
    def preparar(self):
        return {"estado":"registro_notas_empresas", "contenido":self}
    
    def __str__(self):
        return '''
    ID Registro: {}
    Rut Empresa: {}
    Correo: {}
    Fecha Creacion {}
    notas: {}
    '''.format(self.id_registro, self.rut_empresa,
               self.correo, self.fecha_creacion, self.notas)
    
