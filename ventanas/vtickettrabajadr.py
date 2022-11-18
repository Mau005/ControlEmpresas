from ventanas.widgets_predefinidos import MDScreenAbstrac
from ventanas.widgets_predefinidos import MenuEntidades


class GenTicketTrabajador(MDScreenAbstrac):

    def activar(self):
        super().activar()
        self.network.enviar({"estado":"buscar_servicio_id"})

    def actualizar(self, dt):
        super().actualizar(dt)

    def siguiente(self, *dt):
        super().siguiente(dt)

    def volver(self):
        super().volver()

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.coleccion_estados = MenuEntidades(self.network, "Estado:", "Estado:",
                                               self.ids.estado)
