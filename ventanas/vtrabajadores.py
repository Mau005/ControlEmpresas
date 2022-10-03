from kivymd.uix.bottomsheet import MDListBottomSheet

from ventanas.widgets_predefinidos import MDScreenAbstrac, Notificacion
from kivy.properties import ObjectProperty
from core.constantes import BUTTONCREATE
from entidades.registrotrabajador import RegistroTrabajador
from entidades.menuitems import MenuItemLocales, MenuItemPersonas
from ventanas.widgets_predefinidos import MenuEntidades


class VTrabajadores(MDScreenAbstrac):
    botones_trabajadores = ObjectProperty()

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.data = BUTTONCREATE
        self.fecha_inicio = None
        self.fecha_termino = None
        self.botones_trabajadores.data = self.data
        self.correo = "prueba"
        self.persona_actual = ""
        self.local_actual = ""
        self.lista_personas = {}
        self.lista_locales = {}

        self.colecciones_personas = MenuEntidades(self.network, "Rut:", "Rut:", self.ids.botton_rut_accion)
        self.colecciones_locales = MenuEntidades(self.network, "Local:", "Local:", self.ids.botton_id_local,
                                                 filtro="int")

    def accion_boton(self, arg):
        print(arg.icon)
        if arg.icon == "delete":
            self.formatear()
            self.botones_trabajadores.on_close()
        if arg.icon == "exit-run":
            self.botones_trabajadores.on_close()
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
                noti.text = f"Se ha generado correctamente el trabajdor {self.persona_actual}"

            elif info.get("condicion") == "privilegios":
                noti.tex = "Lo lamento no tienes los privilegios suficientes para crear un trabajador"

            self.formatear()
            noti.open()

    def formatear(self):
        self.persona_actual = ""
        self.local_actual = ""
        self.ids.botton_rut_accion.text = "Rut: "
        self.ids.botton_id_local.text = "Local: "
        self.ids.sueldo_trabajador.text = ""
        self.ids.dia_pago.text = ""
        self.activar()

    def activar(self):
        self.colecciones_personas.generar_consulta("menu_personas")
        self.colecciones_locales.generar_consulta("menu_locales")
        super().activar()

    def callback_menu_personas(self, arg):
        procesar = arg.text.split(":")
        objeto = self.lista_personas[procesar[1].replace(" ", "")]
        self.persona_actual = objeto.rut
        self.ids.botton_rut_accion.text = f"Rut:  {self.persona_actual} {objeto.nombre}"

    def callback_menu_locales(self, arg):
        objeto = arg.text.split(":")
        objeto_procesar = self.lista_locales[int(objeto[0])]
        self.local_actual = objeto_procesar.id_local
        self.ids.botton_id_local.text = f"Local: {objeto_procesar.nombre_local}"

    def actualizar(self, *dt):
        return super().actualizar(*dt)

    def siguiente(self, *dt):
        return super().siguiente(*dt)

    def volver(self, *dt):
        return super().volver(*dt)
