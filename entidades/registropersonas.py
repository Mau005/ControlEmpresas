

class RegistroPersonas():
    #RUT_PERSONA	NOMBRES	APELLIDOS	TELEFONO	CELULAR	CORREO
    def __init__(self, **kargs):
        self.rut = kargs.get("rut")
        self.nombres = kargs.get("nombres")
        self.apellidos = kargs.get("apellidos")
        self.telefono = kargs.get("telefono")
        self.celular = kargs.get("celular")
        self.correo = kargs.get("correo")
        
        
    def preparar(self):
        return {"estado":"registropersona", "contenido":self}
    
    

if __name__ == "__main__":
    test = RegistroPersonas(rut = "18.881.495-x", nombres = "Mauricio Andres", apellidos = "Pino Gonzalez")
    preparado = test.preparar()
    print(preparado["estado"])
    print(preparado["contenido"].nombres)
    