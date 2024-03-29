

class RegistrarGastos:
#	id_gasto	descripcion	saldo	fecha_creacion	id_departamento	id_estado_gastos

    def __init__(self, **kargs):
        self.id_gasto = kargs.get("id_gasto")
        self.descripcion = kargs.get("descripcion")
        self.saldo = kargs.get("saldo")
        self.fecha_creacion = kargs.get("fecha_creacion")
        self.id_departamento = kargs.get("id_departamento")
        self.id_estado_gastos = kargs.get("id_estado_gastos")
        self.rut_persona = kargs.get("rut_trabajador")

    def __str__(self) -> str:
        return """
        ID Gasto: {}
        Descripcion: {}
        Saldo: {}
        Fecha Creacion: {}
        Id Departamento: {}
        id Estado Gastos: {}
        Rut Trabajador: {}
        """.format(self.id_gasto, self.descripcion, self.saldo,
                   self.fecha_creacion, self.id_departamento, self.id_estado_gastos,self.rut_persona)

    def preparar(self) -> dict:
        return {"estado":"registrar_gasto", "contenido":self}