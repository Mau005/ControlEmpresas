

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

class Orden_Trabajos_Historia:
    def __init__(self, **kargs):
        self.id_orden = kargs.get("id_orden")
        self.fecha_creacion = kargs.get("fecha_creacion")
        self.id_preparativo_anterior = kargs.get("preparativo_aterior")
        self.id_preparativo_nuevo =kargs.get("preparativo_nuevo")
        self.descripcion = kargs.get("descripcion")