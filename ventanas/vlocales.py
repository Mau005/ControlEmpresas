from entidades.registrarlocales import RegistrarLocales
from ventanas.widgets_predefinidos import MDScreenAbstrac, Notificacion
from kivy.properties import ObjectProperty
from core.constantes import BUTTONCREATE, PROTOCOLOERROR


class VLocales(MDScreenAbstrac):
    botones_locales = ObjectProperty()

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)

        self.botones_locales.data = BUTTONCREATE

    def formatear(self):
        self.ids.nombre_local.text = ""
        self.ids.telefono.text = ""
        self.ids.direccion.text = ""

    def accion_boton(self, arg):
        self.botones_locales.close_stack()
        if arg.icon == "exit-run":
            self.siguiente()

        if arg.icon == "delete":
            self.formatear()

        if arg.icon == "pencil":
            objeto = RegistrarLocales(
                nombre_local=self.ids.nombre_local.text,
                telefono_local=self.ids.telefono.text,
                direccion=self.ids.direccion.text
            )
            self.network.enviar(objeto.preparar())
            info = self.network.recibir()

            print(f"Datos procesados es: {info}")
            if info.get("estado"):
                noti = Notificacion("Correcto", "Se ha registrado correctamente")
                noti.open()
                self.formatear()
                self.siguiente()
                return None

            noti = Notificacion("Error", PROTOCOLOERROR[info.get("condicion")])
            noti.open()
            return None

    def activar(self):
        super().activar()

    def siguiente(self, *dt):
        return super().siguiente(*dt)

    def actualizar(self, *dt):
        return super().actualizar(*dt)

    def volver(self, *dt):
        return super().volver(*dt)
