import kivy
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window

from ventanas.editar_empresa import EditarEmpresa
from ventanas.vlistanotaspersonas import VListaNotasPersonas

from ventanas.vgastos_fechas import VGastosFechas
from ventanas.vlistapersonas import VListasPersonas
from ventanas.vserviciosmensuales import VServiciosMensuales
from ventanas.vtickettrabajadr import GenTicketTrabajador

if kivy.utils.platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.WRITE_EXTERNAL_STORAGE,
                         Permission.READ_EXTERNAL_STORAGE,
                         Permission.INTERNET])
    Builder.load_file("kvlengs/root.kv")
else:
    Window.maximize()
    Builder.load_file("kvlengs_desktop/root.kv")

from ventanas.vlistanotasempresas import VListaNotasEmpresas
from ventanas.vdepartamentos import VDepartamentos
from ventanas.vlocales import VLocales
from ventanas.vnotaspersonas import VNotasPersonas
from network.clientenetwork import ClienteNetwork
from ventanas.entrada import Entrada
from ventanas.casa import Casa
from ventanas.vproductos import VProductos
from ventanas.vpersonas import VPersonas
from ventanas.vempresas import VEmpresas
from ventanas.vnotasempresas import VNotasEmpresas
from ventanas.vlistaempresa import VListasEmpresas
from ventanas.vrecuperacion import VRecuperacion
from ventanas.vlistaproductos import VListaProductos
from ventanas.vtrabajadores import VTrabajadores
from ventanas.vgastos import VGastos
from ventanas.vserviciosdiarios import VServiciosDiarios


class ControlEmpresas(MDApp):
    # Kastachaña: ordenar separar en idioma aymara
    # nohup ./server &
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.theme_cls.theme_style = "Dark"
        # self.theme_cls.primary_palette = "BlueGray"
        self.network = ClienteNetwork()
        self.manejador = MDScreenManager()
        self.__cargar_ventanas()
        Clock.schedule_interval(self.actualizar, 1)

    def __cargar_ventanas(self):
        self.login = Entrada(self.network, self.manejador, "entrada", siguiente="casa")
        self.casa = Casa(self.network, self.manejador, "casa", volver="entrada")
        self.vservicios = VServiciosMensuales(self.network, self.manejador, "serviciosmensuales", siguiente="casa")
        self.vpersonas = VPersonas(self.network, self.manejador, "personas", siguiente="casa")
        self.vempresas = VEmpresas(self.network, self.manejador, "empresas", siguiente="casa")
        self.vnotasempresas = VNotasEmpresas(self.network, self.manejador, "notasempresas", siguiente="casa")
        self.vlistaempresas = VListasEmpresas(self.network, self.manejador, "listaempresas", siguiente="casa")
        self.veditarempresa = EditarEmpresa(self.network, self.manejador, "editar_empresa", siguiente="listaempresas")

        self.vproductos = VProductos(self.network, self.manejador, "productos", siguiente="casa")
        self.vrecuperacion = VRecuperacion(self.network, self.manejador, "recuperacion", volver="entrada")
        self.vlistaproductos = VListaProductos(self.network, self.manejador, "listaproductos", siguiente="casa")
        self.vtrabajadores = VTrabajadores(self.network, self.manejador, "trabajadores", siguiente="casa")
        self.vlocales = VLocales(self.network, self.manejador, "locales", siguiente="casa")
        self.vlistanotasempresas = VListaNotasEmpresas(self.network, self.manejador, "lista_menu_empresas",
                                                       siguiente="casa")
        self.vgrupos = VDepartamentos(self.network, self.manejador, "departamentos",
                                      siguiente="casa")
        self.vnotaspersonas = VNotasPersonas(self.network, self.manejador, "notaspersonas", siguiente="casa")
        self.vgastos = VGastos(self.network, self.manejador, "gastos", siguiente="casa")
        self.vserviciosdiarios = VServiciosDiarios(self.network, self.manejador, "serviciosdiarios", siguiente="casa")
        self.vgastos_fechas = VGastosFechas(self.network, self.manejador, "gastos_fechas", siguiente="casa")
        self.vlistapersonas = VListasPersonas(self.network, self.manejador, "lista_personas", siguiente="casa")

        self.vlistanotaspersonas = VListaNotasPersonas(self.network, self.manejador, "lista_notas_personas",
                                                       siguiente="casa")
        self.vgenticket = GenTicketTrabajador(self.network, self.manejador, "gen_ticket_trabajador", siguiente="casa")

        self.manejador.add_widget(self.login)
        self.manejador.add_widget(self.casa)
        self.manejador.add_widget(self.vservicios)
        self.manejador.add_widget(self.vpersonas)
        self.manejador.add_widget(self.vempresas)
        self.manejador.add_widget(self.vnotasempresas)
        self.manejador.add_widget(self.vlistaempresas)
        self.manejador.add_widget(self.vproductos)
        self.manejador.add_widget(self.vrecuperacion)
        self.manejador.add_widget(self.vlistaproductos)
        self.manejador.add_widget(self.vtrabajadores)
        self.manejador.add_widget(self.vlocales)
        self.manejador.add_widget(self.vlistanotasempresas)
        self.manejador.add_widget(self.vgrupos)
        self.manejador.add_widget(self.vnotaspersonas)
        self.manejador.add_widget(self.vgastos)
        self.manejador.add_widget(self.vserviciosdiarios)
        self.manejador.add_widget(self.vgastos_fechas)
        self.manejador.add_widget(self.vlistapersonas)
        self.manejador.add_widget(self.vlistanotaspersonas)
        self.manejador.add_widget(self.veditarempresa)
        self.manejador.add_widget(self.vgenticket)
        self.login.activar()

    def actualizar(self, dt):
        for ventana in self.manejador.screens:
            ventana.actualizar(dt)

    def cerrar(self):
        self.network.cerrar()

    def build(self):
        self.title = "Kastachana Beta 0.3.0"
        return self.manejador


if __name__ == "__main__":
    test = ControlEmpresas()
    test.run()
    test.cerrar()
