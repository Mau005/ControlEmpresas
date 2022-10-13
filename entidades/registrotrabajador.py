class RegistroTrabajador():

    def __init__(self, **kargs):
        #rut_persona	id_grupo	sueldo	dia_pago
        self.rut_persona = kargs.get("rut_persona")
        self.id_departamento = kargs.get("id_departamento")
        self.sueldo = kargs.get("sueldo")
        self.dia_pago = kargs.get("dia_pago")

    def __str__(self):
        return """
        Rut: {}
        Id Departamento: {}
        Sueldo: {}
        Dia Pago: {}
        """.format(self.rut_persona, self.id_departamento,
                   self.sueldo, self.dia_pago)

    def preparar(self):
        return {"estado": "registrar_trabajador", "contenido": self}
