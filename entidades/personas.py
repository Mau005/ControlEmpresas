class Personas:
    # rut_persona	nombres	apellidos	telefono	celular	correo	id_cuenta
    def __init__(self, **kargs):
        self.rut_persona = kargs.get("rut_persona")
        self.nombres = kargs.get("nombres")
        self.apellidos = kargs.get("apellidos")
        self.telefono = kargs.get("telefono")
        self.celular = kargs.get("celular")
        self.correo = kargs.get("correo")
        self.ubicacion = kargs.get("ubicacion")
        self.rut_empresa = kargs.get("rut_empresa")
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
        return {"estado": "registrar_persona", "contenido": self}


if __name__ == "__main__":
    test = Personas(rut="18.881.495-x", nombres="Mauricio Andres", apellidos="Pino Gonzalez")
    preparado = test.preparar()
    print(preparado["estado"])
    print(preparado["contenido"].nombres)
