from entidades.registrargastos import RegistrarGastos
from ventanas.widgets_predefinidos import MDScreenAbstrac, Notificacion
from core.constantes import PROTOCOLOERROR
from ventanas.widgets_predefinidos import MenuEntidades
from kivymd.uix.pickers import MDDatePicker


class VGastos(MDScreenAbstrac):

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.fecha_asignada = None
        self.coleccion_departamento = MenuEntidades(self.network, "Departamento:",
                                                    "Departamento:", self.ids.departamento, filtro="int")
        self.coleccion_estado_gasto = MenuEntidades(self.network, "Estado Gasto:",
                                                    "Estado Gasto:", self.ids.estado_gasto, filtro="int")

    def crear(self, *args):
        noti = Notificacion("Error", "")

        if self.ids.saldo.text == "":
            noti.text += "Se necesita Ingresar un saldo\n"
        if self.ids.departamento.text == "Departamento:":
            noti.text += "Se necesita seleccionar un departamento\n"
        if self.ids.estado_gasto.text == "Estado Gasto:":
            noti.text += "Se necesita ingresar un estado de gastos\n"
        if self.fecha_asignada is None:
            noti.text += "Debe indicar una fecha de cuando se realizo el gasto\n"

        if len(noti.text) >= 1:
            noti.open()
            return None

        objeto = RegistrarGastos(
            descripcion=self.ids.descripcion.text,
            saldo=int(self.ids.saldo.text),
            fecha_creacion=str(self.fecha_asignada),
            id_departamento=self.coleccion_departamento.dato_guardar,
            id_estado_gastos=self.coleccion_estado_gasto.dato_guardar
        )
        self.network.enviar(objeto.preparar())
        info = self.network.recibir()

        if info.get("estado"):
            noti.title = "Correcto"
            noti.text = "Se ha registrado correctamente"
            noti.open()
            self.formatear()
            return None

        noti.text = PROTOCOLOERROR[info.get("condicion")]
        noti.open()
        return None

    def salir(self, *args):
        self.siguiente()

    def abrir_fecha(self):
        capturar_fecha = MDDatePicker()
        capturar_fecha.bind(on_save=self.guardar_fecha)
        capturar_fecha.open()

    def guardar_fecha(self, instancia, valor, rango_fechas):
        self.fecha_asignada = rango_fechas[0]
        self.ids.fecha_creacion.text = f"Fecha Creación: {self.fecha_asignada}"

    def formatear(self, *args):
        self.ids.departamento.text = "Departamento:"
        self.ids.estado_gasto.text = "Estado Gasto:"
        self.ids.saldo.text = ""
        self.ids.descripcion.text = ""
        self.ids.fecha_creacion.text = "Fecha Creación: 00/00/00"
        self.fecha_asignada = None

    def accion_boton(self, *arg):
        self.ids.botones_gastos.close_stack()

    def activar(self):
        super().activar()
        self.coleccion_departamento.generar_consulta("menu_departamentos")
        self.coleccion_estado_gasto.generar_consulta("menu_estado_gastos")

    def siguiente(self, *dt):
        return super().siguiente(*dt)

    def actualizar(self, *dt):
        return super().actualizar(*dt)

    def volver(self, *dt):
        return super().volver(*dt)
