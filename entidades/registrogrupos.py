class RegistroGrupos:
    def __init__(self, **kargs):
        self.id_grupo = kargs.get("id_grupo")
        self.nombre_grupo = kargs.get("nombre_grupo")
        self.desc = kargs.get("desc")

    def __str__(self):
        return """
        ID Grupo: {}
        Nombre Grupo: {}
        Descripcion: {}
        """.format(self.id_grupo, self.nombre_grupo, self.desc)

    def preparar(self):
        return {"estado": "registrar_grupo", "contenido": self}
