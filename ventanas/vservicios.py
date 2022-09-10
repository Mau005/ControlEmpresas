
from tkinter import E
from ventanas.widgets_predefinidos import MDScreenAbstrac
from kivymd.uix.pickers import MDDatePicker
from kivy.properties import ObjectProperty
import datetime
class VServicios(MDScreenAbstrac):
    nombre = ObjectProperty()
    descr = ObjectProperty()
    estado = ObjectProperty()
    precio = ObjectProperty()
    botones_servicios = ObjectProperty()
        
    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.set_activo(True)
        self.data = {
            'Crear': 'pencil',
            'Formatear': 'language-php',
            'Salir': 'language-cpp',
        }
        self.fecha_inicio = None
        self.fecha_final = None
        self.botones_servicios.data = self.data
        
        
        
    def test(self, arg):
        print(arg.icon)
        if arg.icon == "language-php":
            self.formatear()

    def formatear(self):
        self.fecha_final = None
        self.fecha_final = None
        self.nombre.text = ""
        self.descr.text = ""
        self.precio.text = ""
        self.ids.btn_fecha.text = "00/00/00 al 00/00/00"
    
    
    def abrir_fecha(self):
        date_dialog = MDDatePicker(mode="range")
        date_dialog.bind(on_cancel = self.on_cancel, on_save = self.on_save )
        date_dialog.open()
        
    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

        
    def on_save(self, instance, value, date_range):
        if len(date_range) >= 2:
            self.fecha_inicio = date_range[0]
            self.fecha_final = date_range[-1]
            formato = f"{self.fecha_inicio} al {self.fecha_final}"
            self.ids.btn_fecha.text = str(formato)
        else:
            self.fecha_inicio = value
            self.fecha_final = None
            self.ids.btn_fecha.text = str(value)
        
    def actualizar(self, *dt):
        return super().actualizar(*dt)
    
    def siguiente(self, *dt):
        return super().siguiente(*dt)
    
    def volver(self, *dt):
        return super().volver(*dt)
        
    