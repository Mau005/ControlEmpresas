from kivymd.uix.bottomsheet import MDListBottomSheet

from ventanas.widgets_predefinidos import MDScreenAbstrac, Notificacion
from kivy.properties import ObjectProperty
from core.constantes import BUTTONCREATE
from entidades.registrotrabajador import RegistroTrabajador
from ventanas.widgets_predefinidos import MenuEntidades


class VTrabajadores(MDScreenAbstrac):
    botones_trabajadores = ObjectProperty()

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.data = BUTTONCREATE
        self.fecha_inicio = None
        self.fecha_termino = None
        self.botones_trabajadores.data = self.data

        self.colecciones_personas = MenuEntidades(self.network, "Rut:", "Rut:", self.ids.botton_rut_accion)
        self.colecciones_locales = MenuEntidades(self.network, "Local:", "Local:", self.ids.botton_id_local,
                                                 filtro="int")

    def accion_boton(self, arg):
        print(arg.icon)
        if arg.icon == "delete":
            self.formatear()
        if arg.icon == "exit-run":
            self.siguiente()
        if arg.icon == "pencil":

            objeto = RegistroTrabajador(
                rut=self.colecciones_personas.dato_guardar,
                id_local=self.colecciones_locales.dato_guardar,
                sueldo=int(self.ids.sueldo_trabajador.text),
                dia_pago=int(self.ids.dia_pago.text)
            )
            self.network.enviar(objeto.preparar())
            info = self.network.recibir()
            noti = Notificacion("Error", "Usuario ya se encuentra registrado en Trabajadores")
            if info.get("estado"):
                noti.title = "Correcto"
                noti.text = f"Se ha generado correctamente el trabajdor"

            elif info.get("condicion") == "privilegios":
                noti.tex = "Lo lamento no tienes los privilegios suficientes para crear un trabajador"

            self.formatear()
            noti.open()
        self.botones_trabajadores.close_stack()
    def formatear(self):
        self.ids.botton_rut_accion.text = "Rut: "
        self.ids.botton_id_local.text = "Local: "
        self.ids.sueldo_trabajador.text = ""
        self.ids.dia_pago.text = ""
        self.activar()

    def activar(self):
        self.colecciones_personas.generar_consulta("menu_personas")
        self.colecciones_locales.generar_consulta("menu_locales")
        super().activar()

    def actualizar(self, *dt):
        return super().actualizar(*dt)

    def siguiente(self, *dt):
        return super().siguiente(*dt)

    def volver(self, *dt):
        return super().volver(*dt)
