
class RegistroCuentas:
    def __init__(self, **kargs):
        # id_cuenta	nombre_cuenta	contraseña	fecha_creacion	acceso
        self.id_cuenta = kargs.get("id_cuenta")
        self.nombre_cuenta = kargs.get("nombre_cuenta")
        self.contraseña = kargs.get("contraseña")
        self.fecha_creacion = kargs.get("fecha_creacion")
        self.acceso = kargs.get("acceso")
        self.serializacion = kargs.get("serializacion")

    def __str__(self):
        return """
        ID Cuenta: {}
        Nombre Cuenta: {}
        Contraseña: {}
        Fecha Creacion: {}
        Acceso: {}
        """.format(self.id_cuenta, self.nombre_cuenta, self.contraseña, self.fecha_creacion, self.acceso)

    def preparar(self):
        return {"estado":"registro_cuenta", "contenido":self}
