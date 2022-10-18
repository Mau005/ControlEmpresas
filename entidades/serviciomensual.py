from entidades.abstracservicio import AbstracServicio


class ServicioMensual(AbstracServicio):
    def __init__(self, **kargs):
        AbstracServicio.__init__(self, kargs)
        self.fecha_inicio = kargs.get("fecha_inicio")
        self.fecha_termino = kargs.get("fecha_termino")

    def preparar(self):
        return {"estado": "servicio_mensual", "contenido": self}

    def __str__(self):
        return super().__str__() + """
        Fecha Inicio: {}
        Fecha Termino: {}
        """.format(self.fecha_inicio, self.fecha_termino)
