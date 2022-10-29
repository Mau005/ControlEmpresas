import os

from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.textfield import MDTextField

from core.herramientas import Herramientas as her
from core.constantes import PROTOCOLOERROR
from ventanas.widgets_predefinidos import MDScreenAbstrac, MenuEntidades, Notificacion, ItemContable, ControlArchivos


class VGastosFechas(MDScreenAbstrac):

    def actualizar(self, dt):
        super().actualizar(dt)

    def siguiente(self, *dt):
        super().siguiente(dt)

    def volver(self):
        self.formatear()
        super().volver()

    def activar(self):
        self.coleccion_departamentos.generar_consulta("menu_departamentos")
        super().activar()

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.coleccion_departamentos = MenuEntidades(self.network, "Departamento:", "Departamento:",
                                                     self.ids.departamentos)
        self.lista_datos = []
        self.gastototal = 0
        self.columnas = ["ID", "Tipo", "Saldo", "Usuario", "Departamento", "Fecha Creación", "Total"]
        self.fecha_inicio = None
        self.fecha_termino = None

        self.archivo = ControlArchivos(funcion=self.exportar)

    def desplegar_fechas(self):
        fecha = MDDatePicker(mode="range")
        fecha.bind(on_save=self.guardar_fecha)
        fecha.open()

    def guardar_fecha(self, instancia, valor, rango_fecha):
        if len(rango_fecha) >= 2:
            self.fecha_inicio = rango_fecha[0]
            self.fecha_termino = rango_fecha[-1]
            self.ids.rango_fechas.text = f"{str(self.fecha_inicio)} al {str(self.fecha_termino)}"
            return
        self.fecha_inicio = rango_fecha[0]
        self.fecha_termino = None
        self.ids.rango_fechas.text = f"{str(self.fecha_inicio)} al Sin Asignar"
        return

    def crear(self, *arg):
        if self.ids.rango_fechas.text == "00/00/00 al 00/00/00":
            noti = Notificacion("Error", "Debe indicar almenos una fecha\n")
            noti.open()

        estructura = {"estado": "listado_gastos_fechas",
                      "fecha_inicio": str(self.fecha_inicio),
                      "fecha_termino": str(self.fecha_termino) if self.fecha_termino is not None else None,
                      "departamento": self.coleccion_departamentos.dato_guardar}

        self.network.enviar(estructura)
        info = self.network.recibir()
        self.ids.contenedor_gastos.clear_widgets()
        self.lista_datos.clear()
        self.gastototal = 0
        if info.get("estado"):
            for elementos in info.get("datos"):
                self.lista_datos.append(elementos)
                self.ids.contenedor_gastos.add_widget(
                    ItemContable(elementos[0], elementos[1], elementos[2], elementos[3], elementos[4], elementos[5]))
                self.gastototal += elementos[2]

            self.ids.total_gastos.text = f"Total Gasto: {self.gastototal}"
            return

        noti = Notificacion("Error", PROTOCOLOERROR[info.get("condicion")])
        noti.open()
        return

    def desplegar_archivos(self):
        self.archivo.file_manager_open()

    def exportar(self, *args):

        if len(self.ids.contenedor_gastos.children) == 0:
            noti = Notificacion("Error", "Para poder exportar un excel debe haber contenido en las tablas.")
            noti.open()
            return

        if self.archivo.captura_archivo.campo.text == "":
            noti = Notificacion("Error", "Tiene que indicar un nombre del archivo")
            noti.open()
            return

        self.lista_datos.append([None, None, None, None, None, None, self.gastototal])
        her.generar_excel(self.archivo.ruta, self.archivo.captura_archivo.campo.text, self.lista_datos, self.columnas)

    def formatear(self, *args):
        self.ids.rango_fechas.text = "00/00/00 al 00/00/00"
        self.ids.departamentos.text = "Departamento:"
        self.ids.contenedor_gastos.clear_widgets()
        self.ids.total_gastos.text = "Total Gasto:"
        self.fecha_termino = None
        self.fecha_inicio = None
        self.lista_datos = []
        self.gastototal = 0
        self.coleccion_departamentos.dato_guardar = None
