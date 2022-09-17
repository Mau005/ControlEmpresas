from ventanas.widgets_predefinidos import MDScreenAbstrac
from ventanas.widgets_predefinidos import Notificacion
from core.herramientas import Herramientas as her

class VRecuperacion(MDScreenAbstrac):

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)

    def siguiente(self, *dt):
        super().siguiente(dt)

    def volver(self, *dt):
        self.formatear()
        super().volver(dt)

    def actualizar(self, dt):
        super().actualizar(dt)

    def formatear(self):
        self.ids.contraseña.text = ""
        self.ids.contraseña2.text = ""

    def cambiar_contraseña(self):
        noti = Notificacion("Error", "")
        if len(self.ids.contraseña.text) >= 5:

            if self.ids.contraseña.text == self.ids.contraseña2.text:
                self.network.enviar({"datos": "nueva_contraseña", "contenido": her.cifrado_sha1(self.ids.contraseña.text)})
                info = self.network.recibir()
                if info.get("estado"):
                    noti.title = "Exito"
                    noti.text = "Se ha cambiado la contraseña con exito"
                else:
                    noti.title = "Error"
                    noti.text = info.get("contenido")

            else:
                noti.text = "Contraseñas puestas equivocadamente"
        else:
            noti.text = "La longitud de la contraseña debe ser almenos de 5 caracteres"

        noti.open()
