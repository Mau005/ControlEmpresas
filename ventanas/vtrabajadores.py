from ventanas.widgets_predefinidos import MDScreenAbstrac, Notificacion
from entidades.registrotrabajador import RegistroTrabajador
from ventanas.widgets_predefinidos import MenuEntidades


class VTrabajadores(MDScreenAbstrac):

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.colecciones_personas = MenuEntidades(self.network, "Rut Trabajador:", "Rut Trabajador:",
                                                  self.ids.botton_rut_accion)
        self.colecciones_departamentos = MenuEntidades(self.network, "Departamento:", "Departamento:",
                                                       self.ids.botton_id_departamento,
                                                       filtro="int")

    def crear(self, *args):
        if self.ids.botton_rut_accion.text == "Rut Trabajador:":
            noti = Notificacion("Error", "Debe seleccionar a una persona")
            noti.open()
            return
        if self.ids.botton_id_departamento.text == "Departamento:":
            noti = Notificacion("Error", "Debe seleccionar un departamento")
            noti.open()
            return
        if self.ids.dia_pago.text == "":
            noti = Notificacion("Error", "Debe asignar un dia de pago entre 1 y 30")
            noti.open()
            return

        if self.ids.sueldo_trabajador.text == "":
            noti = Notificacion("Error", "Debe asignar un sueldo al trabajador")
            noti.open()
            return

        objeto = RegistroTrabajador(
            rut_persona=self.colecciones_personas.dato_guardar,
            id_departamento=self.colecciones_departamentos.dato_guardar,
            sueldo=int(self.ids.sueldo_trabajador.text),
            dia_pago=int(self.ids.dia_pago.text)
        )
        self.network.enviar(objeto.preparar())
        info = self.network.recibir()

        if info.get("estado"):
            noti = Notificacion("Exito", "Se ha registrado el trabajdor con exito")
            noti.open()
            self.formatear()
            return

        noti = Notificacion("Error", info.get("condicion"))
        noti.open()
        return

    def formatear(self, *args):
        self.ids.botton_rut_accion.text = "Rut Trabajador:"
        self.ids.botton_id_departamento.text = "Departamento:"
        self.ids.sueldo_trabajador.text = ""
        self.ids.dia_pago.text = ""
        self.activar()

    def activar(self):
        self.colecciones_personas.generar_consulta("menu_personas")
        self.colecciones_departamentos.generar_consulta("menu_departamentos")
        super().activar()

    def actualizar(self, *dt):
        return super().actualizar(*dt)

    def siguiente(self, *dt):
        self.formatear()
        return super().siguiente(*dt)

    def volver(self, *dt):
        return super().volver(*dt)
