
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.lang import Builder

from network.clientenetwork import ClienteNetwork
from ventanas.entrada import Entrada
from ventanas.casa import Casa
from ventanas.vservicios import VServicios
from ventanas.vpersonas import VPersonas

Builder.load_file("kvlengs/root.kv")

class ControlEmpresas(MDApp):
    #Kastachaña: ordenar separar en idioma aymara
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.network = ClienteNetwork()
        self.manejador = MDScreenManager()
        self.login = Entrada(self.network, self.manejador,"entrada", siguiente="casa")
        self.casa = Casa(self.network, self.manejador, "casa")
        self.vservicios = VServicios(self.network, self.manejador, "servicios", siguiente= "casa")
        self.vpersonas = VPersonas(self.network, self.manejador, "personas", siguiente="casa")
        self.__cargar_ventanas()
        
    def __cargar_ventanas(self):
        self.manejador.add_widget(self.login)
        self.manejador.add_widget(self.casa)
        self.manejador.add_widget(self.vservicios)
        self.manejador.add_widget(self.vpersonas)
        
    def cerrar(self):
        self.network.cerrar()
        
    def build(self):
        self.title = "Kastachaña Beta 0.0000000001"
        return self.manejador
    
if __name__ == "__main__":
    test = ControlEmpresas()
    test.run()
    test.cerrar()