

class RegistroPersonas():
    #RUT_PERSONA	NOMBRES	APELLIDOS	TELEFONO	CELULAR	CORREO
    def __init__(self, **kargs):
        self.rut_persona = kargs.get("rut_persona")
        self.nombres = kargs.get("nombres")
        self.apellidos = kargs.get("apellidos")
        self.telefono = kargs.get("telefono")
        self.celular = kargs.get("celular")
        self.correo = kargs.get("correo")
        
        
    def __str__(self):
        return """
    Rut Persona: {}
    Nombres: {}
    Apellidos: {}
    Telefono: {}
    Celular: {}
    Correo: {}
    """.format(self.rut_persona, self.nombres, self.apellidos, self.telefono, self.celular, self.correo)
        
        
    def preparar(self):
        return {"estado":"registropersona", "contenido":self}
    
    

if __name__ == "__main__":
    test = RegistroPersonas(rut = "18.881.495-x", nombres = "Mauricio Andres", apellidos = "Pino Gonzalez")
    preparado = test.preparar()
    print(preparado["estado"])
    print(preparado["contenido"].nombres)
    