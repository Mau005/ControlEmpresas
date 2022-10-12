from ventanas.widgets_predefinidos import MDScreenAbstrac, MenuEntidades, Notificacion
from core.constantes import BUTTONCREATE, PROTOCOLOERROR
from entidades.registronotas import RegistroNotas


class VNotasEmpresas(MDScreenAbstrac):

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.ids.botones.data = BUTTONCREATE
        self.coleccion_empresas = MenuEntidades(self.network, "Rut Empresa:", "Rut:", self.ids.boton_empresas)

    def accion_boton(self, arg):
        self.ids.botones.close_stack()
        if arg.icon == "pencil":

            if len(self.ids.nota_empresas.text) <= 5:
                noti = Notificacion("Error", "Debe indicar una nota para gestionarla")
                noti.open()
                return
            if self.ids.boton_empresas.text == "Rut Empresa:":
                noti = Notificacion("Error", "Debe indicar que empresa")
                noti.open()
                return

            objeto = RegistroNotas(
                rut_asociado=self.coleccion_empresas.dato_guardar,
                nota=self.ids.nota_empresas.text
            )

            self.network.enviar(objeto.preparar("registro_notas_empresas"))
            info = self.network.recibir()
            if info.get("estado"):
                noti = Notificacion("Exito",
                                    f"Se ha registrado una nota  a la empresa: {self.coleccion_empresas.dato_guardar}")
                noti.open()
                return

            noti = Notificacion("Error",PROTOCOLOERROR(info.get("condicion")))
            noti.open()
            return

        if arg.icon == "delete":
            self.formatear()

        if arg.icon == "exit-run":
            self.siguiente()
            self.formatear()

    def activar(self):
        self.coleccion_empresas.generar_consulta("menu_empresas")
        super().activar()

    def formatear(self):
        self.ids.boton_empresas.text = "Rut Empresa:"
        self.ids.nota_empresas.text = ""
        self.coleccion_empresas.dato_guardar = None

    def siguiente(self, *dt):
        return super().siguiente(*dt)

    def volver(self, *dt):
        return super().volver(*dt)

    def actualizar(self, *dt):
        return super().actualizar(*dt)
