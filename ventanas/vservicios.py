from ventanas.widgets_predefinidos import MDScreenAbstrac, Notificacion, MenuEntidades
from kivymd.uix.pickers import MDDatePicker
from kivy.properties import ObjectProperty
from entidades.registroservicio import RegistroServicios


class MenuItemEstado:
    def __init__(self, id_estado, nombre):
        self.id_estado = id_estado
        self.nombre = nombre


class VServicios(MDScreenAbstrac):
    nombre = ObjectProperty()
    descr = ObjectProperty()
    id_estado = ObjectProperty()
    precio = ObjectProperty()

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.ids.botones_servicios.data = {'Crear': ["pencil", "on_release", self.crear],
                                           'Formatear': ["delete", "on_release", self.formatear],
                                           'Salir': ["exit-run", "on_release", self.siguiente]}
        self.fecha_inicio = None
        self.fecha_termino = None
        self.colecciones_estado = MenuEntidades(self.network, "Estados:", "Id:", self.ids.id_estado, filtro="int")
        self.colecciones_rut_cliente = MenuEntidades(self.network, "Rut Cliente:", "Rut Cliente:",
                                                     self.ids.boton_rut_cliente)
        self.colecciones_rut_trabajador = MenuEntidades(self.network, "Rut Trabajador:", "Rut Trabajador:",
                                                        self.ids.boton_rut_trabajador)

    def crear(self, *args):
        if self.fecha_inicio is None:
            noti = Notificacion("ERROR", "Alemenos debe indicar la fecha de inicio.")
            noti.open()
            return
        if not len(self.precio.text) >= 1:
            noti = Notificacion("Error", "Debe asignar algun precio")
            noti.open()
            return

        if self.fecha_termino is None:
            self.fecha_termino = ""

        obj = RegistroServicios(nombre=self.nombre.text,
                                descr=self.descr.text,
                                fecha_inicio=str(self.fecha_inicio),
                                fecha_termino=str(self.fecha_termino),
                                id_estado=self.colecciones_estado.dato_guardar,
                                precio=int(self.precio.text),
                                rut_persona=self.colecciones_rut_cliente.dato_guardar,
                                rut_trabajador=self.colecciones_rut_trabajador.dato_guardar,
                                )
        self.network.enviar(obj.preparar())
        datos = self.network.recibir()
        if datos.get("estado"):
            test = Notificacion("Exito", datos.get("condicion"))
            test.open()
            self.formatear()
            return
        if datos.get("condicion") == "privilegios":
            test = Notificacion("Error",
                                datos.get("No tienes los privilegios suficientes para crear servicios!"))
            test.open()

    def accion_boton(self, arg):
        self.ids.botones_servicios.close_stack()

    def formatear(self, *args):
        self.fecha_termino = None
        self.fecha_termino = None
        self.nombre.text = ""
        self.id_estado.text = "Estado:"
        self.colecciones_estado.dato_guardar = None
        self.descr.text = ""
        self.precio.text = ""
        self.ids.btn_fecha.text = "00/00/00 al 00/00/00"
        self.ids.boton_rut_cliente.text = "Rut Cliente:"
        self.ids.boton_rut_trabajador.text = "Rut Trabajador:"
        self.colecciones_rut_trabajador.dato_guardar = None
        self.colecciones_rut_cliente.dato_guardar = None
        self.colecciones_estado.dato_guardar = None

    def activar(self):
        self.colecciones_estado.generar_consulta("menu_estado")
        self.colecciones_rut_cliente.generar_consulta("menu_personas")
        self.colecciones_rut_trabajador.generar_consulta("menu_trabajadores")
        super().activar()

    def abrir_fecha(self):
        date_dialog = MDDatePicker(mode="range")
        date_dialog.bind(on_cancel=self.on_cancel, on_save=self.on_save)
        date_dialog.open()

    def on_cancel(self, instance, value):
        """Events called when the "CANCEL" dialog box button is clicked."""

    def on_save(self, instance, value, date_range):
        if len(date_range) >= 2:
            self.fecha_inicio = date_range[0]
            self.fecha_termino = date_range[-1]
            formato = f"{self.fecha_inicio} al {self.fecha_termino}"
            self.ids.btn_fecha.text = str(formato)
        else:
            self.fecha_inicio = value
            self.fecha_termino = None
            self.ids.btn_fecha.text = str(value)

    def actualizar(self, *dt):
        return super().actualizar(*dt)

    def siguiente(self, *dt):
        self.formatear()
        return super().siguiente(*dt)

    def volver(self, *dt):
        return super().volver(*dt)
