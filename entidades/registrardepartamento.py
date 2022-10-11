class RegistrarDepartamento:
    def __init__(self, **kargs):
        self.id_grupo = kargs.get("id_grupo")
        self.nombre_departamento = kargs.get("nombre_departamento")
        self.descripcion = kargs.get("descripcion")
        self.id_local = kargs.get("id_local")

    def __str__(self):
        return """
        ID Grupo: {}
        Nombre Grupo: {}
        Descripcion: {}
        """.format(self.id_grupo, self.nombre_grupo, self.desc)

    def preparar(self):
        return {"estado": "registrar_departamento", "contenido": self}
