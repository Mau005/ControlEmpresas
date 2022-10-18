from entidades.serviciomensual import ServicioMensual
from ventanas.widgets_predefinidos import MDScreenAbstrac, Notificacion, MenuEntidades
from kivymd.uix.pickers import MDDatePicker


class VServiciosMensuales(MDScreenAbstrac):

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.fecha_inicio = None
        self.fecha_termino = None
        self.lista_productos = {}
        self.colecciones_estado = MenuEntidades(self.network, "Estados:", "Estados:", self.ids.id_estado, filtro="int")
        self.colecciones_rut_cliente = MenuEntidades(self.network, "Rut Cliente:", "Rut Cliente:",
                                                     self.ids.boton_rut_cliente)
        self.colecciones_departamentos = MenuEntidades(self.network, "Departamento:", "Departamento:",
                                                       self.ids.boton_departamentos)

        self.colecciones_procutos = MenuEntidades(self.network, "Agregar Producto:", "Agregar Producto:",
                                                       self.ids.boton_departamentos)

    def crear(self, *args):
        noti = Notificacion("Error", "")
        if self.fecha_inicio is None:
            noti.text += "Alemenos debe indicar la fecha de inicio.\n"
        if len(self.ids.nombre.text) <= 3:
            noti.text += "Tiene que indicar un nombre del servicio.\n"

        if self.ids.id_estado.text == "Estados:":
            noti.text += "Tiene que indicar un estado del servicio.\n"

        if self.ids.boton_rut_cliente.text == "Rut Cliente:":
            noti.text += "Tiene que indicar un cliente.\n"

        if self.ids.boton_departamentos.text == "Departamento:":
            noti.text += "Tiene que indicar un departamento.\n"

        if len(self.ids.ubicacion.text) <= 3:
            noti.text += "Tiene que indicar una ubicacion.\n"

        if self.ids.btn_fecha.text == "00/00/00 al 00/00/00":
            noti.text += "Alemenos debe indicar la fecha de inicio.\n"

        if len(self.lista_productos) == 0:
            noti.text += "Tiene que indicar un producto para los servicios.\n"

        if not noti.text == "":
            noti.open()
            return



        obj = ServicioMensual(
            nombre_servicio=self.ids.nombre.text,
            url_posicion=self.ids.url_posicion.text,
            ubicacion=self.ids.ubicacion.text,
            rut_usuario=self.colecciones_rut_cliente.dato_guardar,
            descripcion=self.ids.descr.text,
            id_departamento=self.colecciones_departamentos.dato_guardar,
            fecha_inicio=self.fecha_inicio,
            fecha_termino=self.fecha_termino
        )
        print(obj)
        return
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

    def formatear(self, *args):
        self.fecha_termino = None
        self.fecha_termino = None
        self.ids.nombre.text = ""
        self.ids.id_estado.text = "Estados:"
        self.ids.descr.text = ""
        self.ids.btn_fecha.text = "00/00/00 al 00/00/00"
        self.ids.boton_rut_cliente.text = "Rut Cliente:"
        self.ids.boton_departamentos.text = "Departamento:"
        self.colecciones_departamentos.dato_guardar = None
        self.colecciones_rut_cliente.dato_guardar = None
        self.colecciones_estado.dato_guardar = None

    def activar(self):
        self.colecciones_estado.generar_consulta("menu_estado")
        self.colecciones_rut_cliente.generar_consulta("menu_personas")
        self.colecciones_departamentos.generar_consulta("menu_departamentos")
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
