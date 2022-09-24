from abc import abstractmethod
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import CircularElevationBehavior
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.list import TwoLineListItem, ThreeLineListItem
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFloatingActionButtonSpeedDial


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



    def procesar_colores(self,cantidad):
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


class MDCardPre(MDCard, CircularElevationBehavior):
    pass


class NotificacionText(MDDialog):

    def __init__(self, title, ayuda, aceptar=None, **kargs):
        self.auto_dismiss = True
        self.title = title
        self.campo = MDTextField(hint_text=ayuda, size_hint_x=None, width="240")
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

    @abstractmethod
    def actualizar(self, dt):
        if self.name != "entrada" and self.activo:
            self.network.enviar({"estado": "actualizar", "contenido": self.name})
            info = self.network.recibir()
            if not info.get("estado"):
                noti = Notificacion("Error", info.get("contenido"))
                noti.open()
                self.manager.current = "entrada"
                self.manager.get_screen("entrada").activar()
                self.network.iniciar()

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
