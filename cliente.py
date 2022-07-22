
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder

from network.clientenetwork import ClienteNetwork

Builder.load_file("kvlengs/login.kv")

class Login(Screen):
    
    def __init__(self,network, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.network = network
        
    def enviar_saludo(self):
        self.network.enviar({"estado": "saludo", "contenido": "Hola te hablo del servidor"})
        print(self.network.recibir())
        


class ControlEmpresas(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.network = ClienteNetwork()
        self.login = Login(self.network)
        self.manejador = ScreenManager()
        self.manejador.add_widget(self.login)
        
    def cerrar(self):
        self.network.cerrar()
        
    def build(self):
        return self.manejador
    
if __name__ == "__main__":
    test = ControlEmpresas()
    test.run()
    test.cerrar()