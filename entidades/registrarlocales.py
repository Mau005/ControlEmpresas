

class RegistrarLocales:
#ID_LOCAL, NOMBRE_LOCAL, TELEFONO_LOCAL, DIRECCION

    def __init__(self, **kargs):
        self.id_local = kargs.get("id_local")
        self.nombre_local = kargs.get("nombre_local")
        self.telefono_local = kargs.get("telefono_local")
        self.direccion = kargs.get("direccion")

    def __str__(self):
        return """
        ID Local: {}
        Nombre: {}
        Telefono: {}
        Direccion: {}
        """.format(self.id_local, self.nombre_local,self.telefono_local,self.direccion)

    def preparar(self):
        return {"estado":"registrarlocal", "contenido":self}