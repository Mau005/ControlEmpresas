from ventanas.widgets_predefinidos import MDScreenAbstrac, MenuEntidades, Notificacion
from core.constantes import BUTTONCREATE, PROTOCOLOERROR
from entidades.registronotas import RegistroNotas


class VNotasPersonas(MDScreenAbstrac):

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.ids.botones.data = BUTTONCREATE
        self.coleccion_personas = MenuEntidades(self.network, "Rut Persona:", "Rut Persona:", self.ids.boton_persona)

    def accion_boton(self, arg):
        self.ids.botones.close_stack()
        if arg.icon == "pencil":

            if len(self.ids.nota_persona.text) <= 5:
                noti = Notificacion("Error", "Debe indicar una nota para gestionarla")
                noti.open()
                return
            if self.ids.boton_persona.text == "Rut Persona:":
                noti = Notificacion("Error", "Debe indicar que persona")
                noti.open()
                return

            objeto = RegistroNotas(
                rut_asociado=self.coleccion_personas.dato_guardar,
                nota=self.ids.nota_persona.text
            )

            self.network.enviar(objeto.preparar("registro_notas_personas"))
            info = self.network.recibir()
            if info.get("estado"):
                noti = Notificacion("Exito",
                                    f"Se ha registrado una nota  a la empresa: {self.coleccion_personas.dato_guardar}")
                noti.open()
                return

            noti = Notificacion("Error", PROTOCOLOERROR(info.get("condicion")))
            noti.open()
            return

        if arg.icon == "delete":
            self.formatear()

        if arg.icon == "exit-run":
            self.siguiente()
            self.formatear()

    def activar(self):
        self.coleccion_personas.generar_consulta("menu_personas")
        super().activar()

    def formatear(self):
        self.ids.boton_persona.text = "Rut Persona:"
        self.ids.nota_persona.text = ""
        self.coleccion_personas.dato_guardar = None

    def siguiente(self, *dt):
        return super().siguiente(*dt)

    def volver(self, *dt):
        return super().volver(*dt)

    def actualizar(self, *dt):
        return super().actualizar(*dt)
