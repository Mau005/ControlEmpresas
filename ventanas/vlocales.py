from entidades.registrarlocales import RegistrarLocales
from ventanas.widgets_predefinidos import MDScreenAbstrac, Notificacion
from kivy.properties import ObjectProperty
from core.constantes import BUTTONCREATE

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
        if arg.icon == "exit-run":
            self.siguiente()

        if arg.icon == "delete":
            self.formatear()

        if arg.icon == "pencil":
            objeto = RegistrarLocales(
                nombre_local = self.ids.nombre_local.text,
                telefono_local = self.ids.telefono.text,
                direccion=self.ids.direccion.text
            )
            self.network.enviar(objeto.preparar())
            info = self.network.recibir()
            noti = Notificacion("Error", "")
            print(f"Datos procesados es: {info}")
            if info.get("estado"):
                noti.title= "Correcto"
                noti.text = "Se ha registrado correctamente"
            else:
                if info.get("condicion") == "privilegios":
                    noti.text = "Problemas de Privilegios"
                elif info.get("condicion") == "NETWORK":
                    noti.text = "Se ha desconectado del servidor"
                else:
                    noti.text = f"Error desconocido {info.get('condicion')}"
            noti.open()


    def activar(self):
        super().activar()
    def siguiente(self, *dt):
        return super().siguiente(*dt)

    def actualizar(self, *dt):
        return super().actualizar(*dt)

    def volver(self, *dt):
        return super().volver(*dt)
