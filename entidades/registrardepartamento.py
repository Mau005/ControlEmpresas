class RegistrarDepartamento:
    def __init__(self, **kargs):
        self.id_departamento = kargs.get("id_departamento")
        self.id_local = kargs.get("id_local")
        self.nombre_departamento = kargs.get("nombre_departamento")
        self.descripcion = kargs.get("descripcion")

    def __str__(self) -> str:
        return """
        ID Grupo: {}
        Nombre Grupo: {}
        Descripcion: {}
        """.format(self.id_departamento, self.nombre_departamento, self.descripcion)

    def preparar(self) -> dict:
        return {"estado": "registrar_departamento", "contenido": self}
