
from schema.querys import Querys


class GestionEstados:

    def __init__(self, query:Querys):
        self.query = query
        self.status = []
        self.preparativos = None

    def GenerateStatus(self):

        status = self.query.get_list_status("personas","id_estado", "nombre_estado")
        preparatives = self.querys.get_list_status("")


