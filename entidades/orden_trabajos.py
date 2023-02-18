
class Orden_Trabajos:

    def __init__(self, **kargs):
        self.id_orden = kargs.get("id_orden")
        self.id_servicios = kargs.get("id_servicios")
        self.fecha_creacion = kargs.get("fecha_creacion")
        self.fecha_termino = kargs.get("fecha_termino")
        self.id_estado = kargs.get("id_estado")
        self.id_estados_preparativos = kargs.get("id_preparativos")
        self.precio_ot = kargs.get("precio_ot")
        self.descripcion = kargs.get("descripcion")

    def __str__(self) -> str:
        return f"Id Orde: {self.id_orden}" \
               f"Id Servicios: {self.id_servicios}" \
               f"descripcion: {self.descripcion}"

class Orden_Trabajos_Historia:
    def __init__(self, **kargs):
        self.id_ot_historia = kargs.get("id_ot_historia")
        self.id_orden = kargs.get("id_orden")
        self.fecha_creacion = kargs.get("fecha_creacion")
        self.id_preparativo_anterior = kargs.get("preparativo_aterior")
        self.id_preparativo_nuevo =kargs.get("preparativo_nuevo")
        self.descripcion = kargs.get("descripcion")

    def __str__(self) -> str:
        return """
        Id Orden Historia: {}
        Id Orden: {}
        Fecha Creacion: {}
        Id Preparativo Anterior: {}
        id Preparativo Nuevo: {}
        Descripcion: {}
        """.format(self.id_ot_historia, self.id_orden, self.fecha_creacion, self.id_preparativo_anterior,
                   self.id_preparativo_nuevo, self.descripcion)
