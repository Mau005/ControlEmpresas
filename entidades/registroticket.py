

class RegistroTicket:

    def __init__(self, **kargs):
        # id_ticket	id_servicios	fecha_creacion	fecha_termino	id_estado	descripcion
        self.id_ticket = kargs.get("id_ticket")
        self.id_servicios = kargs.get("id_servicios")
        self.fecha_creacion = kargs.get("fecha_creacion")
        self.id_estado_anterior = kargs.get("id_estado_anterior")
        self.id_estado = kargs.get("id_estado")
        self.descripcion = kargs.get("descripcion")
        self.id_cuenta = kargs.get("cuenta")

    def __str__(self):
        return """
        ID Ticket: {}
        ID Servicio: {}
        Fecha Creacion: {}
        Fecha Termino: {}
        ID Estado Anterior: {}
        ID Estado: {}
        Descripcion: {}
        Cuenta: {}
        """.format(self.id_ticket, self.id_servicios, self.fecha_creacion,
                   self.id_estado_anterior, self.id_estado, self.descripcion, self.id_cuenta)

    def preparar(self):
        return {"estado": "registro_tickets", "contenido": self}
