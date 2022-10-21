from kivymd.uix.bottomsheet import MDListBottomSheet

from core.constantes import PROTOCOLOERROR
from entidades.serviciodiarios import ServicioDiarios
from ventanas.widgets_predefinidos import MDScreenAbstrac, MenuEntidades, Notificacion, MenuEntidadesMultiples
from kivy.properties import ObjectProperty


class VServiciosDiarios(MDScreenAbstrac):

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.toda_la_semana = False
        self.total = 0
        self.coleccion_menu_estados = MenuEntidades(self.network, "Estado:", "Estado:", self.ids.id_estado,
                                                    filtro="int")
        self.coleccion_menu_cliente = MenuEntidades(self.network, "Rut Cliente:", "Rut Cliente:",
                                                    self.ids.boton_rut_cliente)
        self.coleccion_menu_departamentos = MenuEntidades(self.network, "Departamento:", "Departamento:",
                                                          self.ids.boton_departamentos, filtro="int")
        self.menu_productos = MenuEntidadesMultiples(self.network, self.ids.contenedor_objetos,
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
        dias = self.__dias_diarios()

        if len(self.ids.nombre.text) <= 3:
            noti.text += "Tiene que indicar un nombre del servicio.\n"

        if self.ids.id_estado.text == "Estados:":
            noti.text += "Tiene que indicar un estado del servicio.\n"

        if self.ids.boton_rut_cliente.text == "Rut Cliente:":
            noti.text += "Tiene que indicar un cliente.\n"

        if self.ids.boton_departamentos.text == "Departamento:":
            noti.text += "Tiene que indicar un departamento.\n"

        if dias == "":
            noti.text += "Tiene que indicar almenos 1 día de la semana"

        if len(self.ids.ubicacion.text) <= 3:
            noti.text += "Tiene que indicar una ubicacion.\n"

        if len(self.ids.contenedor_objetos.children) == 0:
            noti.text += "Debe indicar un producto almenos\n"

        if self.chequear_objetos(self.ids.contenedor_objetos):
            noti.text += "Los Productos tienen que tener un precio de mayor o igual a 0 y una cantidad minima de 1"

        if not noti.text == "":
            noti.open()
            return

        servicio_diario = ServicioDiarios(
            nombre_servicio=self.ids.nombre.text,
            url_posicion=self.ids.url_posicion.text,
            ubicacion=self.ids.ubicacion.text,
            id_estado=self.coleccion_menu_estados.dato_guardar,
            rut_usuario=self.coleccion_menu_cliente.dato_guardar,
            descripcion=self.ids.descr.text,
            id_departamento=self.coleccion_menu_departamentos.dato_guardar,
            dias_diarios=dias
        )
        paquete = servicio_diario.preparar()

        productos = []
        for elementos in self.ids.contenedor_objetos.children:
            productos.append(elementos.generar())

        paquete.update({"productos": productos})
        self.network.enviar(paquete)

        info = self.network.recibir()
        if info.get("estado"):
            noti.title = "Exito"
            noti.text = f"Se ha registrado con exito el servidio: {servicio_diario.nombre_servicio}"
            noti.open()
            return
        noti.text = PROTOCOLOERROR[info.get("condicion")]
        noti.open()
        return

    def __dias_diarios(self):
        dias_diarios = ""
        if self.ids.lunes.active:
            dias_diarios += "1"
        if self.ids.martes.active:
            dias_diarios += "2"
        if self.ids.miercoles.active:
            dias_diarios += "3"
        if self.ids.jueves.active:
            dias_diarios += "4"
        if self.ids.viernes.active:
            dias_diarios += "5"
        if self.ids.sabado.active:
            dias_diarios += "6"
        if self.ids.domingo.active:
            dias_diarios += "7"
        return dias_diarios

    def formatear(self):
        self.ids.nombre.text = ""
        self.ids.id_estado.text = "Estados:"
        self.ids.boton_rut_cliente.text = "Rut Cliente:"
        self.ids.boton_departamentos.text = "Departamento:"
        self.ids.url_posicion.text = ""
        self.ids.ubicacion.text = ""
        self.ids.descr.text = ""
        self.ids.lunes.active = False
        self.ids.martes.active = False
        self.ids.miercoles.active = False
        self.ids.jueves.active = False
        self.ids.viernes.active = False
        self.ids.sabado.active = False
        self.ids.domingo.active = False
        self.ids.contenedor_objetos.clear_widgets()
        self.coleccion_menu_departamentos.dato_guardar = None
        self.coleccion_menu_cliente.dato_guardar = None
        self.coleccion_menu_estados.dato_guardar = None

    def activar(self):
        super().activar()
        self.coleccion_menu_estados.generar_consulta("menu_estado")
        self.coleccion_menu_cliente.generar_consulta("menu_personas")
        self.coleccion_menu_departamentos.generar_consulta("menu_departamentos")
        self.menu_productos.generar_consulta("menu_productos")

    def actualizar(self, *dt):
        if self.activo:
            self.actualizar_total()
        return super().actualizar(*dt)

    def siguiente(self, *dt):
        self.formatear()
        return super().siguiente(*dt)

    def volver(self, *dt):
        return super().volver(*dt)
