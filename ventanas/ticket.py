from kivymd.uix.boxlayout import MDBoxLayout

from entidades.registroticket import RegistroTicket


class Ticket(MDBoxLayout):

    def __init__(self, **kargs):
        super().__init__(**kargs)
        # id_ticket	id_servicios	fecha_creacion	fecha_termino	id_estado	descripcion

    def generar_objeto(self) -> RegistroTicket:
        return RegistroTicket(
            id_ticket=self.ids.id_ticket,
            id_servicios=self.ids.id_servicios,
            fecha_creacion=self.ids.fecha_creacion,
            id_estado_anterior=self.ids.id_estado_anterior,
            id_estado=self.ids,
            descripcion=self.ids.descripcion
        )
