class RegistroTrabajador():

    def __init__(self, **kargs):
        self.rut = kargs.get("rut")
        self.id_local = kargs.get("id_local")
        self.sueldo = kargs.get("sueldo")
        self.dia_pago = kargs.get("dia_pago")

    def __str__(self):
        return """
        Rut: {}
        Id Local: {}
        Sueldo: {}
        Dia Pago: {}
        """.format(self.rut, self.id_local, self.sueldo, self.dia_pago)

    def preparar(self):
        return {"estado": "registrartrabajador", "contenido": self}
