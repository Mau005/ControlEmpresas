from entidades.registrarlocales import RegistrarLocales
from ventanas.widgets_predefinidos import MDScreenAbstrac, Notificacion
from core.constantes import PROTOCOLOERROR


class VLocales(MDScreenAbstrac):

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)

        self.ids.botones_locales.data = {'Crear': ["pencil", "on_release", self.crear],
                                         'Formatear': ["delete", "on_release", self.formatear],
                                         'Salir': ["exit-run", "on_release", self.siguiente]}

    def crear(self, *args):
        objeto = RegistrarLocales(
            nombre_local=self.ids.nombre_local.text,
            telefono_local=self.ids.telefono.text,
            direccion=self.ids.direccion.text
        )
        self.network.enviar(objeto.preparar())
        info = self.network.recibir()
        if info.get("estado"):
            noti = Notificacion("Correcto", "Se ha registrado correctamente")
            noti.open()
            self.formatear()
            self.siguiente()
            return None

        noti = Notificacion("Error", PROTOCOLOERROR[info.get("condicion")])
        noti.open()
        return None

    def formatear(self, *args):
        self.ids.nombre_local.text = ""
        self.ids.telefono.text = ""
        self.ids.direccion.text = ""

    def accion_boton(self, arg):
        self.ids.botones_locales.close_stack()

    def activar(self):
        super().activar()

    def siguiente(self, *dt):
        return super().siguiente(*dt)

    def actualizar(self, *dt):
        return super().actualizar(*dt)

    def volver(self, *dt):
        return super().volver(*dt)
