from entidades.registrogrupos import RegistroGrupos
from ventanas.widgets_predefinidos import MDScreenAbstrac, Notificacion
from kivy.properties import ObjectProperty
from core.constantes import BUTTONCREATE, PROTOCOLOERROR
from kivy.logger import Logger


class VGrupos(MDScreenAbstrac):
    botones = ObjectProperty()

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)

        self.botones.data = BUTTONCREATE

    def formatear(self):
        self.ids.nombre_local.text = ""
        self.ids.telefono.text = ""
        self.ids.direccion.text = ""

    def accion_boton(self, arg):
        self.botones.close_stack()
        if arg.icon == "exit-run":
            self.siguiente()

        if arg.icon == "delete":
            self.formatear()

        if arg.icon == "pencil":
            noti = Notificacion("Error", "")
            if len(self.ids.nombre_grupo.text) <= 5:
                noti.text += "Nombre de grupo almenos debe tener 5 caracteres\n"
                noti.open()
                return

            objeto = RegistroGrupos(
                nombre_grupo=self.ids.nombre_grupo.text,
                desc=self.ids.desc_grupo.text
            )
            self.network.enviar(objeto.preparar())
            info = self.network.recibir()
            if info.get("estado"):
                noti.open()
                return
            if info.get("condicion") == "NETWORK":
                noti.text = PROTOCOLOERROR["NETWORK"]
                noti.open()
                return
        Logger.critical(f"Error no contralado en VGrupos datos: {info}")

    def formatear(self):
        self.ids.nombre_grupo.text = ""
        self.ids.desc_grupo.text = ""


    def activar(self):
        super().activar()

    def siguiente(self, *dt):
        return super().siguiente(*dt)

    def actualizar(self, *dt):
        return super().actualizar(*dt)

    def volver(self, *dt):
        return super().volver(*dt)
