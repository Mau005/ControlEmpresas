from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from abc import abstractmethod
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.textfield import MDTextField


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

    def guardado(self):
        self.mensaje_capturado = self.campo.text

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
        self.__activo = False

    def set_activo(self, condicion):
        if isinstance(condicion, bool):
            self.__activo = condicion

    def get_activo(self):
        return self.__activo

    @abstractmethod
    def actualizar(self, *dt):
        pass

    @abstractmethod
    def siguiente(self, *dt):
        if self.nombre_siguiente:
            self.manager.current = self.nombre_siguiente

    @abstractmethod
    def volver(self, *dt):
        if self.nombre_volver:
            self.manager.current = self.nombre_volver
