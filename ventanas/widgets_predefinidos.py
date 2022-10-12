from abc import abstractmethod

from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import RectangularElevationBehavior

from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.list import TwoLineListItem, ThreeLineListItem, MDList
from kivymd.uix.textfield import MDTextField

from entidades.menuitems import MenuGlobal
from entidades.registronotas import RegistroNotas


class MenuEntidades:

    def __init__(self, network, nombre_boton, nombre_busqueda, boton_modificar, filtro="str"):
        """
        Clase definida para crear multiples consulta de botones para seleccionar
        cosas, soporta 2 argumentos de retorno
        """
        self.nombre_boton = nombre_boton
        self.nombre_busqueda = nombre_busqueda
        self.network = network
        self.boton_modificar = boton_modificar
        self.listados = {}
        self.dato_guardar = None
        self.filtro = filtro
        self.boton_modificar.bind(on_release=self.desplegar_menu)
        self.actualizado = False

    def __limpiada(self):
        self.listados.clear()

    def __conversion(self):
        if self.filtro == "int":
            self.dato_guardar = int(self.dato_guardar)
        elif self.filtro == "float":
            self.dato_guardar = float(self.dato_guardar)
        elif self.filtro == "bool":
            self.dato_guardar = bool(self.dato_guardar)
        elif self.filtro == "str":
            if isinstance(self.dato_guardar, str):
                if len(self.dato_guardar) == 0:
                    self.dato_guardar = None

    def formateo(self):
        self.actualizado = False
        self.dato_guardar = None

    def callback(self, arg):
        procesar = arg.text.split(":")
        identificador = procesar[1].split("\n")

        objeto = self.listados.get(identificador[0].replace(" ", ""))
        self.dato_guardar = objeto.identificador
        self.boton_modificar.text = f"{self.nombre_boton} {identificador[0]}\n{identificador[1]}"
        self.__conversion()
        self.actualizado = True

    def desplegar_menu(self, *args):
        bottom_sheet_menu = MDListBottomSheet()
        for objetos in self.listados.values():
            bottom_sheet_menu.add_item(f"{self.nombre_busqueda} {objetos.identificador}\n{objetos.nombre}",
                                       self.callback)
        bottom_sheet_menu.open()

    def generar_consulta(self, consultar):
        self.__limpiada()
        self.network.enviar({"estado": consultar})
        info = self.network.recibir()
        if info.get("estado"):
            for elementos in info.get("datos"):
                objeto = MenuGlobal(str(elementos[0]), elementos[1])
                self.listados.update({objeto.identificador: objeto})
            return {"estado": True}
        return {"estado": False, "condicion": "CONSULTA"}


class MDTreeLine(ThreeLineListItem):

    def __init__(self, id_identificador, nombres, cantidad, network, **kargs):
        super().__init__(**kargs)
        self.network = network
        self.id_identificador = id_identificador
        self.nombres = nombres
        self.cantidad = cantidad
        self.text = str(self.id_identificador)
        self.secondary_text = f"Nombre: {self.nombres}"
        self.tertiary_text = f"Cantidad: {self.cantidad}"
        self.procesar_colores(cantidad)

    def procesar_colores(self, cantidad):
        self.tertiary_theme_text_color = "Custom"
        if cantidad >= 0 and cantidad <= 3:
            self.tertiary_text_color = [1, 0, 0, 1]
        elif cantidad >= 4 and cantidad <= 10:
            self.tertiary_text_color = [0, .5, 0, 1]
        elif cantidad >= 11:
            self.tertiary_text_color = [0, 1, 0, 1]


class MDTwoLine(TwoLineListItem):
    def __init__(self, titulo, contenido, network, **kwargs):
        super().__init__(**kwargs)
        self.text = titulo
        self.secondary_text = contenido
        self.network = network


class MDCardPre(MDCard, RectangularElevationBehavior):
    pass


class NotificacionText(MDDialog):

    def __init__(self, title, ayuda, aceptar=None, **kargs):
        self.auto_dismiss = True
        self.title = title
        self.campo = MDTextField(hint_text=ayuda, size_hint_x=None, width="350")
        self.mensaje_capturado = ""
        self.botonCancelar = MDRoundFlatButton(text="Cancelar", on_release=self.cancelar)
        self.botonAceptar = MDRoundFlatButton(text="Aceptar", on_release=self.cancelar)
        if aceptar is not None:
            self.botonAceptar.bind(on_release=aceptar)

        self.buttons = [self.botonCancelar, self.botonAceptar]

        super().__init__(**kargs)
        self.add_widget(self.campo)

    def cancelar(self, *args):
        self.dismiss()


class Notificacion(MDDialog):

    def __init__(self, titulo, mensaje, funcion_concurrente=None, **kwargs):
        self.title = titulo
        self.text = mensaje
        self.auto_dismiss = True
        self.aceptar = MDRoundFlatButton(text="Aceptar", on_release=self.salir)
        self.cancelar = MDRoundFlatButton(text="Cancelar", on_release=self.salir)
        self.buttons = [self.aceptar, self.cancelar]

        if funcion_concurrente is not None:
            self.aceptar.bind(on_release=funcion_concurrente)

        super().__init__(**kwargs)

    def salir(self, *Arg):
        self.dismiss()


class MDScreenAbstrac(MDScreen):

    @abstractmethod
    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(**kw)
        self.name = nombre
        self.network = network
        self.manejador = manejador
        self.nombre_siguiente = siguiente
        self.nombre_volver = volver
        self.activo = False

    @abstractmethod
    def activar(self):
        self.desactivar_ventanas()
        self.activo = True

    def desactivar_ventanas(self):
        for elementos in self.manager.screen_names:
            self.manager.get_screen(elementos).activo = False

    def __desconectar(self):
        self.manager.current = "entrada"
        self.manager.get_screen("entrada").activar()
        self.network.iniciar()

    @abstractmethod
    def actualizar(self, dt):
        if self.name != "entrada" and self.activo:
            self.network.enviar({"estado": "actualizar", "contenido": self.name})
            info = self.network.recibir()
            if not info.get("estado"):
                noti = Notificacion("Error", info.get("contenido"))
                noti.open()
                self.__desconectar()

    @abstractmethod
    def siguiente(self, *dt):
        if self.nombre_siguiente:
            self.manager.get_screen(self.nombre_siguiente).activar()
            self.manager.current = self.nombre_siguiente

    @abstractmethod
    def volver(self):
        if self.nombre_volver:
            self.manejador.get_screen(self.nombre_volver).activar()
            self.manager.current = self.nombre_volver


class ItemCard(MDCardPre):
    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.elevation = 15
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(400)
        self.padding = dp(20)
        self.adaptative_size = True
        self.contenedor = MDList(size_hint_y=None, size = self.size )
        self.add_widget(self.contenedor)



class ItemNotaEmpresa(ItemCard):
    def __init__(self, network, objeto, **kargs):
        super().__init__(**kargs)

        maqueta = RegistroNotas()
        maqueta.__dict__ = objeto.__dict__
        self.network = network

        self.scroll = ScrollView(do_scroll_x=False, do_scroll_y=True, size_hint_y= None, height=dp(100))
        self.id_registro = MDTextField(hint_text="ID Registro", text=str(maqueta.id_registro), disabled=True, mode= "fill")
        self.nota = MDTextField(hint_text="Nota", text=maqueta.nota, multiline=True, disabled=True)
        self.rut_empresa = MDTextField(hint_text="Rut Empresa:", text=maqueta.rut_asociado, disabled=True)
        self.correo = MDTextField(hint_text="Usuario", text=maqueta.id_cuenta, disabled=True)
        self.fecha_creacion = MDTextField(hint_text="Fecha Creación", text=str(maqueta.fecha_creacion), disabled=True)

        self.contenedor.add_widget(self.id_registro)
        self.scroll.add_widget(self.nota)
        self.contenedor.add_widget(self.scroll)
        self.contenedor.add_widget(self.rut_empresa)
        self.contenedor.add_widget(self.correo)
        self.contenedor.add_widget(self.fecha_creacion)
