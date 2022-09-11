

class RegistroPersonas():
    #RUT_PERSONA	NOMBRES	APELLIDOS	TELEFONO	CELULAR	CORREO
    def __init__(self, **kargs):
        self.rut = kargs.get("rut")
        self.nombres = kargs.get("nombres")
        self.apellidos = kargs.get("apellidos")
        self.telefono = kargs.get("telefono")
        self.celular = kargs.get("celular")
        self.correo = kargs.get("correo")