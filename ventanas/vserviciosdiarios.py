from kivymd.uix.bottomsheet import MDListBottomSheet

from ventanas.widgets_predefinidos import MDScreenAbstrac, Notificacion
from kivymd.uix.pickers import MDDatePicker
from kivy.properties import ObjectProperty
from entidades.registroservicio import RegistroServicios
from core.constantes import BUTTONCREATE


class MenuItemEstado():
    def __init__(self, id_estado, nombre):
        self.id_estado = id_estado
        self.nombre = nombre


class VServiciosDiarios(MDScreenAbstrac):
    nombre = ObjectProperty()
    descr = ObjectProperty()
    id_estado = ObjectProperty()
    precio = ObjectProperty()
    botones_servicios = ObjectProperty()

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.data = BUTTONCREATE
        self.botones_servicios.data = self.data
        self.correo = "prueba"
        self.servicio_actual = 1  # por defecto bd es operativo
        self.lista_estados = {}

    def accion_boton(self, arg):
        print(arg.icon)
        if arg.icon == "delete":
            self.formatear()
        if arg.icon == "exit-run":
            self.botones_servicios.on_close()
            self.siguiente()
        if arg.icon == "pencil":
           pass

    def formatear(self):
        self.nombre.text = ""
        self.id_estado.text = "Estado"
        self.descr.text = ""
        self.precio.text = ""

    def activar(self):
        self.lista_estados.clear()  # limpiamos el menu de informacion clonada
        self.network.enviar({"estado": "estadoservicios"})
        info = self.network.recibir()

        for elementos in info.get("datos"):
            objeto = MenuItemEstado(elementos[0], elementos[1])
            self.lista_estados.update({objeto.nombre: objeto})
        super().activar()

    def callback_menu(self, arg):
        self.servicio_actual = self.lista_estados[arg.text].id_estado
        self.id_estado.text = f"Estado: {arg.text}"

    def desplegar_menu(self):
        bottom_sheet_menu = MDListBottomSheet()
        for objetos in self.lista_estados.keys():
            bottom_sheet_menu.add_item(objetos, self.callback_menu)
        bottom_sheet_menu.open()

    def actualizar(self, *dt):
        return super().actualizar(*dt)

    def siguiente(self, *dt):
        return super().siguiente(*dt)

    def volver(self, *dt):
        return super().volver(*dt)
