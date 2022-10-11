

class RegistroEmpresas:
    #rut_empresa	nombre_empresa	giro_empresa	direccion_empresa
    # correo_empresa	correo_respaldo	telefono_empresa	celular_empresa
    def __init__(self, **kargs):
        self.rut_empresa = kargs.get("rut_empresa")
        self.nombre_empresa = kargs.get("nombre_empresa")
        self.giro_empresa = kargs.get("giro_empresa")
        self.direccion_empresa = kargs.get("direccion_empresa")
        self.telefono_empresa = kargs.get("telefono_empresa")
        self.correo_empresa = kargs.get("correo_empresa")
        self.correo_respaldo = kargs.get("correo_respaldo")
        self.celular_empresa = kargs.get("celular_empresa")
        
    def preparar(self):
        return {"estado": "registro_empresa", "contenido":self}
        
    def __str__(self):
        return '''
    Rut_Empresa: {}
    Nombre_Empresa: {}
    Giro Empresa: {}
    Direccion Empresa: {}
    Telefono: {}
    Correo Empresa: {}
    Correo Respaldo: {}
    Celular empresa: {}
    '''.format(self.rut_empresa, self.nombre_empresa, self.giro_empresa,
               self.direccion_empresa, self.telefono_empresa, self.correo_empresa,
               self.correo_empresa, self.celular_empresa)

        
if __name__ == "__main__":
    test = RegistroEmpresas(rut_empresa = "11123123")
    print(type(test.correo_empresa))