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
from core.herramientas import Herramientas as her
from ventanas.vnotasempresas import VNotasEmpresas
from ventanas.vlistaempresa import VListasEmpresas

Builder.load_file("kvlengs/root.kv")

class ControlEmpresas(MDApp):
    #Kastachaña: ordenar separar en idioma aymara
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        self.network = ClienteNetwork()
        self.manejador = MDScreenManager()
        
        self.login = Entrada(self.network, self.manejador,"entrada", siguiente="casa")
        self.casa = Casa(self.network, self.manejador, "casa")
        self.vservicios = VServicios(self.network, self.manejador, "servicios", siguiente= "casa")
        self.vpersonas = VPersonas(self.network, self.manejador, "personas", siguiente="casa")
        self.vempresas = VEmpresas(self.network, self.manejador, "empresas", siguiente = "casa")
        self.vnotasempresas = VNotasEmpresas(self.network, self.manejador, "notasempresas",siguiente = "casa")
        self.vlistaempresas = VListasEmpresas(self.network, self.manejador, "listaempresas", siguiente="casa")
        self.vlistaservicios = VListadoServicios(self.network, self.manejador, "listaservicios", siguiente="casa")
        self.vproductos = VProductos(self.network, self.manejador, "productos", siguiente="casa")
        self.__cargar_ventanas()
        
    def __cargar_ventanas(self):
        self.manejador.add_widget(self.login)
        self.manejador.add_widget(self.casa)
        self.manejador.add_widget(self.vservicios)
        self.manejador.add_widget(self.vpersonas)
        self.manejador.add_widget(self.vempresas)
        self.manejador.add_widget(self.vnotasempresas)
        self.manejador.add_widget(self.vlistaempresas)
        self.manejador.add_widget(self.vlistaservicios)
        self.manejador.add_widget(self.vproductos)
        
    def cerrar(self):
        self.network.cerrar()
        
    def build(self):
        self.title = "Kastachaña Beta 0.2.1"
        return self.manejador
    
if __name__ == "__main__":
    test = ControlEmpresas()
    test.run()
    test.cerrar()