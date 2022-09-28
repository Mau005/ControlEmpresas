from datetime import datetime
from core.constantes import DIA_SEMANA



class Calendario_Notificaciones():
    def __init__(self):
        self.dia_actual = DIA_SEMANA[datetime.isoweekday(datetime.now())]

    def consultar_dia(self, año, mes, dia):
        return DIA_SEMANA[datetime.isoweekday(datetime(año, mes, dia))]

    def consultar_dia_isoformato(self, año, mes, dia):
        return datetime(año, mes, dia).isoformat()

    def consultar_fechas(self,date1, date2):
        print(date1-date2)

    def actualizar(self, dt):
        self.dia_actual = DIA_SEMANA[datetime.isoweekday(datetime.now())]

class Testeo:

    def __init__(self, **kargs):
        self.nombre = kargs.get("nombre")

    def __eq__(self, other):
        self.nombre = other.nombre


if __name__ == "__main__":
    pass