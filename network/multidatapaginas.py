

from core.herramientas import Herramientas as her
class MultiDataPaginas:

    def __init__(self,**kargs):
        """
        Secuencias: IDUnico,
        """
        self.cliente = kargs.get("cliente")
        self.bd = kargs.get("bd")
        self.cuenta = kargs.get("cuenta")
        self.trabajador = kargs.get("trabajador")
        self.PagesDirection = {}
        self.Services = kargs.get("querys")


    def ControlSecuencias(self, **kargs):
        pass


    def BuscarServicios(self, **kargs):
        where = "WHERE "
        querys = """
        SELECT id_servicios, nombre_servicio, ubicacion
        FROM servicios
        WHERE id_estado = 1 OR id_estado = 2
        """