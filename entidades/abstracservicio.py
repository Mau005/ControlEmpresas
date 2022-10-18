from abc import abstractmethod, ABC


class AbstracServicio(ABC):
    #	id_servicios	nombre_servicio	id_estado	url_posicion
    #	ubicacion	rut_usuario	descripcion	id_departamento	fecha_creacion
    @abstractmethod
    def __init__(self, **kargs):
        self.id_servicio = kargs.get("id_servicio")
        self.nombre_servicio = kargs.get("nombre_servicio")
        self.id_estado = kargs.get("id_estado")
        self.url_posicion = kargs.get("url_posicion")
        self.ubicacion = kargs.get("ubicacion")
        self.rut_usuario = kargs.get("rut_usuario")
        self.descripcion = kargs.get("descripcion")
        self.id_departamento = kargs.get("id_departamento")
        self.fecha_creacion = kargs.get("fecha_creacion")

    @abstractmethod
    def preparar(self):
        pass

    @abstractmethod
    def __str__(self):
        return """
        ID Servicio: {}
        Nombre Servicio: {}
        ID Estado: {}
        URL Posicion: {}
        Ubicacion: {}
        Rut Usuario: {}
        Descripcion: {}
        ID Departamento: {}
        Fecha Creacion: {}
        """.format(self.id_servicio, self.nombre_servicio, self.id_estado,
                   self.url_posicion, self.ubicacion, self.rut_usuario,
                   self.descripcion, self.id_departamento, self.fecha_creacion)
