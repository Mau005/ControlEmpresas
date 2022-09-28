

class RegistroServiciosDiarios():

    def __init__(self, **kargs):
        self.id_servicios_diarios = kargs.get("id_servicios_diarios")
        self.nombre_servicio = kargs.get("nombre_servicio")
        self.id_estado = kargs.get("id_estado")
        self.precio = kargs.get("precio")
        self.fecha_semana = kargs.get("fecha_semana")
        self.url_posicion = kargs.get("url_posicion")
        self.ubicacion = kargs.get("ubicacion")
        self.rut_usuario = kargs.get("rut_usuario")
        self.rut_trabajador = kargs.get("rut_trabajador")
        self.descr = kargs.get("descr")
        self.toda_semana = kargs.get("toda_semana")
        # ID_SERVICIOS_DIARIOS	NOMBRE_SERVICIO	ID_ESTADO	PRECIO	FECHA_SEMANA
        # #URL_POSICION	UBICACION	RUT_USUARIO	RUT_TRABAJADOR	DESCR	TODA_SEMANA

    def __str__(self):
        return """
        ID Servicio: {}
        Nombre Servicio: {}
        ID Estado: {}
        Precio: {}
        Fecha Semana: {}
        Url Posicion: {}
        Ubicacion: {}
        Rut Usuario: {}
        Rut Trabajador: {}
        Descr: {}
        Toda Semana: {}
        """.format(self.id_servicios_diarios, self.nombre_servicio, self.id_estado, self.precio, self.fecha_semana,
                   self.url_posicion, self.ubicacion, self.rut_usuario, self.rut_trabajador, self.descr,
                   self.toda_semana)

    def preparar(self):
        return {"estado":"registroserviciodiario", "contenido": self}

