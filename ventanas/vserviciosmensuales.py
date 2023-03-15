from core.constantes import PROTOCOLOERROR
from entidades.serviciomensual import ServicioMensual
from ventanas.widgets_predefinidos import MDScreenAbstrac, Notificacion, MenuEntidades, MenuEntidadesMultiples
from kivymd.uix.pickers import MDDatePicker


class VServiciosMensuales(MDScreenAbstrac):

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.fecha_inicio = None
        self.fecha_termino = None
        self.total = 0
        self.colecciones_rut_cliente = MenuEntidades(self.network, "Rut Cliente:", "Rut Cliente:",
                                                     self.ids.boton_rut_cliente)
        self.colecciones_departamentos = MenuEntidades(self.network, "Departamento:", "Departamento:",
                                                       self.ids.boton_departamentos)

        self.colecciones_productos = MenuEntidadesMultiples(self.network, self.ids.contenedor_objetos,
                                                            self.ids.btn_agregar_productos)

    def actualizar_total(self):
        if len(self.ids.contenedor_objetos.children) == 0:
            self.total = 0
            self.ids.neto.text = f"NETO: {self.total}"
            self.ids.iva.text = f"IVA: {self.total * 0.19}"
            self.ids.total_servicio_mensual.text = f"Total: {self.total * 1.19}"

        self.total = 0
        for objetos in self.ids.contenedor_objetos.children:
            elemento = objetos.generar()
            if elemento is not None:
                resultado = elemento.precio * elemento.cantidad
                self.total += resultado
                self.ids.neto.text = f"NETO: {self.total}"
                self.ids.iva.text = f"IVA: {self.total * 0.19}"
                self.ids.total_servicio_mensual.text = f"Total: {self.total * 1.19}"

    def chequear_objetos(self, contenedor):
        for elementos in contenedor.children:
            objeto = elementos.generar()
            if objeto is None:
                return True
        return False

    def crear(self, *args):
        noti = Notificacion("Error", "")
        if self.fecha_inicio is None:
            noti.text += "Alemenos debe indicar la fecha de inicio.\n"

        if self.fecha_termino is None:
            noti.text += "Tiene que tener una fecha de Termino.\n"

        if len(self.ids.nombre.text) <= 3:
            noti.text += "Tiene que indicar un nombre del servicio.\n"

        if self.ids.boton_rut_cliente.text == "Rut Cliente:":
            noti.text += "Tiene que indicar un cliente.\n"

        if self.ids.boton_departamentos.text == "Departamento:":
            noti.text += "Tiene que indicar un departamento.\n"

        if len(self.ids.ubicacion.text) <= 3:
            noti.text += "Tiene que indicar una ubicacion.\n"

        if self.ids.btn_fecha.text == "00/00/00 al 00/00/00":
            noti.text += "Alemenos debe indicar la fecha de inicio.\n"

        if len(self.ids.contenedor_objetos.children) == 0:
            noti.text += "Debe indicar un producto almenos"

        if self.chequear_objetos(self.ids.contenedor_objetos):
            noti.text += "Los Productos tienen que tener un precio de mayor o igual a 0 y una cantidad minima de 1"

        if not noti.text == "":
            noti.open()
            return
        obj = ServicioMensual(
            nombre_servicio=self.ids.nombre.text,
            url_posicion=self.ids.url_posicion.text,
            ubicacion=self.ids.ubicacion.text,
            id_estado=1,
            rut_usuario=self.colecciones_rut_cliente.dato_guardar,
            descripcion=self.ids.descr.text,
            id_departamento=self.colecciones_departamentos.dato_guardar,
            fecha_inicio=self.fecha_inicio,
            fecha_termino=self.fecha_termino
        )
        productos = []
        for elementos in self.ids.contenedor_objetos.children:
            productos.append(elementos.generar())

        paquete = obj.preparar()
        paquete.update({"productos":productos})

        self.network.enviar(paquete)
        datos = self.network.recibir()

        if datos.get("estado"):
            noti.title= "Exito"
            noti.text = "Se ha generado el servicio con exito"
            noti.open()
            self.formatear()
            return
        if datos.get("condicion") == "privilegios":
            noti.text = PROTOCOLOERROR[datos.get("condicion")]
            noti.open()

    def formatear(self, *args):
        self.fecha_inicio = None
        self.fecha_termino = None
        self.ids.nombre.text = ""
        self.ids.descr.text = ""
        self.ids.ubicacion.text = ""
        self.ids.btn_fecha.text = "00/00/00 al 00/00/00"
        self.ids.boton_rut_cliente.text = "Rut Cliente:"
        self.ids.boton_departamentos.text = "Departamento:"
        self.colecciones_departamentos.dato_guardar = None
        self.colecciones_rut_cliente.dato_guardar = None
        self.ids.contenedor_objetos.clear_widgets()

    def activar(self):
        self.colecciones_rut_cliente.generar_consulta("menu_personas")
        self.colecciones_departamentos.generar_consulta("menu_departamentos")
        self.colecciones_productos.generar_consulta("listadoproductos")
        super().activar()

    def abrir_fecha(self):
        date_dialog = MDDatePicker(mode="range")
        date_dialog.bind(on_cancel=self.on_cancel, on_save=self.on_save)
        date_dialog.open()

    def on_cancel(self, instance, value):
        """Events called when the "CANCEL" dialog box button is clicked."""

    def on_save(self, instancia, fecha_actual, rango_fechas):
        if len(rango_fechas) >= 2:
            self.fecha_inicio = str(rango_fechas[0])
            self.fecha_termino = str(rango_fechas[-1])
            formato = f"{self.fecha_inicio} al {self.fecha_termino}"
            self.ids.btn_fecha.text = str(formato)
        else:
            self.fecha_inicio = str(rango_fechas[0])
            self.fecha_termino = None
            self.ids.btn_fecha.text = str(rango_fechas[0])

    def actualizar(self, *dt):
        if self.activo:
            self.actualizar_total()
        return super().actualizar(*dt)

    def siguiente(self, *dt):
        self.formatear()
        return super().siguiente(*dt)

    def volver(self, *dt):
        return super().volver(*dt)
