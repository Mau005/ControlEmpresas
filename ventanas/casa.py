from kivy.uix.screenmanager import FadeTransition
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelThreeLine, MDExpansionPanelOneLine

from ventanas.widgets_predefinidos import MDScreenAbstrac
from kivy.properties import ObjectProperty


class Contenido(MDBoxLayout):
    pass


class Casa(MDScreenAbstrac):
    lista_productos = ObjectProperty()

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.mis_servicios = None
        self.mis_trabajos = None
        self.ids.manejador_menus.transition = FadeTransition()

    def activar_servicios(self):
        """
        TODO: desabilitado hasta tener los sitema de ordenes de trabajo
        """
        self.network.enviar({"estado": "mis servicios"})
        info = self.network.recibir()

        if info.get("estado"):
            if not len(info.get("datos")) == 0:
                self.mis_servicios = MDExpansionPanel(
                    icon="arrow-right-bold-hexagon-outline",
                    content=Contenido(orientation="vertical"),
                    panel_cls=MDExpansionPanelOneLine(
                        text="Mis Servicios",
                    )
                )
                self.ids.contenedor_notificaciones.add_widget(self.mis_servicios)
                for elementos in info.get("datos"):
                    self.mis_servicios.content.add_widget(
                        MDExpansionPanelThreeLine(
                            text=f"Servicio {elementos[0]} {elementos[2]}",
                            secondary_text=f"Usuario: {elementos[1]} Fecha Creación: {elementos[3]}",
                            tertiary_text=f"Estado: {elementos[5]}"
                        )
                    )

    def activar_servicios_trabajador(self):
        """
        TODO: desabilitado el sistema de trabajadores, para poder gestionar mejor las ordenes de trabajo
        """
        self.network.enviar({"estado": "mis trabajos"})
        info = self.network.recibir()

        if info.get("estado"):
            if not len(info.get("datos")) == 0:
                self.mis_trabajos = MDExpansionPanel(
                    icon="arrow-right-bold-hexagon-outline",
                    content=Contenido(orientation="vertical"),
                    panel_cls=MDExpansionPanelOneLine(
                        text="Mis Trabajos",
                    )
                )
                self.ids.contenedor_notificaciones.add_widget(self.mis_trabajos)
                for elementos in info.get("datos"):
                    self.mis_trabajos.content.add_widget(
                        MDExpansionPanelThreeLine(
                            text=f"Servicio {elementos[0]} {elementos[1]} Estado: {elementos[9]}",
                            secondary_text=f"Ubicación: {elementos[3]}",
                            tertiary_text=f"Descripción: {elementos[4]}"
                        )
                    )

    def activar(self):
        self.ids.contenedor_notificaciones.clear_widgets()
        #self.activar_servicios()
        #self.activar_servicios_trabajador()

    def cambiar_screen(self, name):
        self.ids.manejador_menus.current = name


    def crear_servicios(self):
        self.manager.current = "servicios"

    def crear_usuarios(self):
        self.manager.current = "personas"

    def cambiar_ventanta(self, ventana):
        self.manager.get_screen(ventana).activar()
        self.manager.current = ventana

    def salir(self, *Arg):
        self.volver()
        self.network.enviar({"estado": "desconectar"})

    def actualizar(self, *dt):
        return super().actualizar(*dt)

    def siguiente(self, *dt):
        return super().siguiente(*dt)

    def volver(self, *dt):
        return super().volver(*dt)
