from kivy.core.window import Window

from ventanas.VListaNotasEmpresas import VListaNotasEmpresas
from ventanas.vdepartamentos import VDepartamentos
from ventanas.vlocales import VLocales
from ventanas.vnotaspersonas import VNotasPersonas

Window.size = (400, 625)
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.lang import Builder

from network.clientenetwork import ClienteNetwork
from ventanas.entrada import Entrada
from ventanas.casa import Casa
from ventanas.vlistadoservicios import VListadoServicios
from ventanas.vproductos import VProductos
from ventanas.vservicios import VServicios
from ventanas.vpersonas import VPersonas
from ventanas.vempresas import VEmpresas
from ventanas.vnotasempresas import VNotasEmpresas
from ventanas.vlistaempresa import VListasEmpresas
from ventanas.vrecuperacion import VRecuperacion
from ventanas.vlistaproductos import VListaProductos
from ventanas.vserviciosdiarios import VServiciosDiarios
from ventanas.vtrabajadores import VTrabajadores
from kivy.clock import Clock

Builder.load_file("kvlengs/root.kv")


class ControlEmpresas(MDApp):
    # Kastachaña: ordenar separar en idioma aymara

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.network = ClienteNetwork()
        self.manejador = MDScreenManager()
        self.__cargar_ventanas()
        Clock.schedule_interval(self.actualizar, 1)

    def __cargar_ventanas(self):
        self.login = Entrada(self.network, self.manejador, "entrada", siguiente="casa")
        self.casa = Casa(self.network, self.manejador, "casa", volver="entrada")
        self.vservicios = VServicios(self.network, self.manejador, "servicios", siguiente="casa")
        self.vpersonas = VPersonas(self.network, self.manejador, "personas", siguiente="casa")
        self.vempresas = VEmpresas(self.network, self.manejador, "empresas", siguiente="casa")
        self.vnotasempresas = VNotasEmpresas(self.network, self.manejador, "notasempresas", siguiente="casa")
        self.vlistaempresas = VListasEmpresas(self.network, self.manejador, "listaempresas", siguiente="casa")
        self.vlistaservicios = VListadoServicios(self.network, self.manejador, "listaservicios", siguiente="casa")
        self.vproductos = VProductos(self.network, self.manejador, "productos", siguiente="casa")
        self.vrecuperacion = VRecuperacion(self.network, self.manejador, "recuperacion", volver="entrada")
        self.vlistaproductos = VListaProductos(self.network, self.manejador, "listaproductos", siguiente="casa")
        self.vserviciosdiarios = VServiciosDiarios(self.network, self.manejador, "serviciosdiarios", siguiente="casa")
        self.vtrabajadores = VTrabajadores(self.network, self.manejador, "trabajadores", siguiente="casa")
        self.vlocales = VLocales(self.network, self.manejador, "locales", siguiente="casa")
        self.vlistanotasempresas = VListaNotasEmpresas(self.network, self.manejador, "lista_menu_empresas",
                                                       siguiente="casa")
        self.vgrupos = VDepartamentos(self.network, self.manejador, "departamentos",
                                      siguiente="casa")
        self.vnotaspersonas = VNotasPersonas(self.network, self.manejador, "notaspersonas", siguiente="casa")

        self.manejador.add_widget(self.login)
        self.manejador.add_widget(self.casa)
        self.manejador.add_widget(self.vservicios)
        self.manejador.add_widget(self.vpersonas)
        self.manejador.add_widget(self.vempresas)
        self.manejador.add_widget(self.vnotasempresas)
        self.manejador.add_widget(self.vlistaempresas)
        self.manejador.add_widget(self.vlistaservicios)
        self.manejador.add_widget(self.vproductos)
        self.manejador.add_widget(self.vrecuperacion)
        self.manejador.add_widget(self.vlistaproductos)
        self.manejador.add_widget(self.vserviciosdiarios)
        self.manejador.add_widget(self.vtrabajadores)
        self.manejador.add_widget(self.vlocales)
        self.manejador.add_widget(self.vlistanotasempresas)
        self.manejador.add_widget(self.vgrupos)
        self.manejador.add_widget(self.vnotaspersonas)
        self.login.activar()

    def actualizar(self, dt):
        for ventana in self.manejador.screens:
            ventana.actualizar(dt)

    def cerrar(self):
        self.network.cerrar()

    def build(self):
        self.title = "Kastachaña Beta 0.2.1"
        return self.manejador


if __name__ == "__main__":
    test = ControlEmpresas()
    test.run()
    test.cerrar()
