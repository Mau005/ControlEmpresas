from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from abc import abstractmethod
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFloatingActionButtonSpeedDial


class MDTwoLine(TwoLineListItem):
    def __init__(self, titulo, contenido, network, **kwargs):
        super().__init__(**kwargs)
        self.text = titulo
        self.secondary_text = contenido
        self.network = network


class MDCardPre(MDCard, RoundedRectangularElevationBehavior):
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
            self.network.enviar({"estado": "actualizar","contenido":self.name})
            info = self.network.recibir()
            if not info.get("estado"):
                noti = Notificacion("Error",  info.get("contenido"))
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
