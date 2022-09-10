from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from abc import abstractmethod
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRoundFlatButton

from kivymd.uix.list import OneLineListItem

class MDCardPre(MDCard, RoundedRectangularElevationBehavior):
    pass


class NotificacionLobby(OneLineListItem):
    
    def __init__(self, nombre ,funcion_concurrente = None, **kwargs):
        super().__init__(**kwargs)
        
        if funcion_concurrente != None:
            self.on_release = funcion_concurrente
                        
        
    

class Notificacion(MDDialog):
    
    def __init__(self,titulo, mensaje, funcion_concurrente = None,  **kwargs):
        super().__init__(**kwargs)
        
        self.title = titulo
        self.text = mensaje
        self.aceptar = MDRoundFlatButton(text = "Aceptar", on_release = self.salir)
        self.cancelar = MDRoundFlatButton(text = "Cancelar",  on_release = self.salir)
        self.buttons = [self.aceptar, self.cancelar]
        
        if funcion_concurrente != None:
            self.aceptar.bind(on_release = funcion_concurrente)
            
        
        self.create_buttons() #actualiza los widget de el array de buttones

        
    def salir(self, *Arg):
        self.dismiss()
        

    

class MDScreenAbstrac(MDScreen):
    
    @abstractmethod
    def __init__(self, network, manejador, nombre, siguiente = None, volver = None, **kw):
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
            self.manager.current= self.nombre_siguiente
    
    @abstractmethod
    def volver(self, *dt):
        if self.nombre_volver:
            self.manager.current = self.nombre_volver