
class Cuentas:
    def __init__(self, **kargs):
        # id_cuenta	nombre_cuenta	contraseña	fecha_creacion	acceso
        self.rut_persona = kargs.get("rut_persona")
        self.nombre_cuenta = kargs.get("nombre_cuenta")
        self.contraseña = kargs.get("contraseña")
        self.fecha_creacion = kargs.get("fecha_creacion")
        self.acceso = kargs.get("acceso") if kargs.get("acceso") != None else 0
        self.serializacion = kargs.get("serializacion") # arugento para indicar un usuario activo.

    def __str__(self) -> str:
        return """
        Rut_persona: {}
        Nombre Cuenta: {}
        Contraseña: {}
        Fecha Creacion: {}
        Acceso: {}
        """.format(self.rut_persona, self.nombre_cuenta, self.contraseña, self.fecha_creacion, self.acceso)

    def preparar(self) -> dict:
        return {"estado":"registro_cuenta", "contenido":self}

if __name__ == "__main__":
    test = Cuentas(acceso = 4)
    test2 = Cuentas(rut_persona="hola")
    print(test)
    print(test2)