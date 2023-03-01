
class Estados:

    def __init__(self, **kargs):
        """
        Method procured id status, and preparatives
        """
        self.id_estado = kargs.get("id_estado")
        self.nombre  = kargs.get("nombre")


    def __str__(self):
        return """
        ID: {}
        Nombre: {}
        """.format(self.id_estado, self.nombre)