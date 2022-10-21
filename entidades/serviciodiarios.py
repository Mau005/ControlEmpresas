from entidades.abstracservicio import AbstracServicio


class ServicioDiarios(AbstracServicio):

    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.dias_diarios = kargs.get("dias_diarios")

    def __str__(self):
        return super().__str__() + """
        Dias Diarios: {}
        """.format(self.dias_diarios)

    def preparar(self):
        return {"estado": "registro_servicio_diario", "contenido": self}
