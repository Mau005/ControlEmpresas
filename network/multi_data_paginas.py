from socket import socket
from schema.querys import Querys


class MultiDataPaginas:

    def __init__(self,querys:Querys, cliente:socket, **kargs):
        """
        Secuencias: IDUnico,
        """
        self.cliente = cliente
        self.PagesDirection = {}
        self.querys = querys


    def ControlSecuencias(self, **kargs):
        pass

    def Gestion_Paginas(self, data):
        if data.get("algo"):
            pass


    def BuscarServicios(self, data):
        list_keys = []
        ascendente = False
        for key, value in data.items:
            if key == "ascendente":
                ascendente = key
            if value == 0 and key != "ascendente":
                continue
            list_keys.append(value)

        cantidad

        where = "id_estado = "
        querys = """
        SELECT id_servicios, nombre_servicio, ubicacion
        FROM servicios
        WHERE id_estado = 1 OR id_estado = 2
        """