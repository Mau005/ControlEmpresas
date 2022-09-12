from entidades.registropersonas import RegistroPersonas
from ventanas.widgets_predefinidos import MDScreenAbstrac, Notificacion
from kivy.properties import ObjectProperty

class VPersonas(MDScreenAbstrac):
    botones = ObjectProperty()
    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.data = {
            'Crear': 'pencil',
            'Formatear': 'delete',
            'Salir': 'exit-run',
        }
        self.botones.data = self.data
        
    def formatear(self):
        self.ids.rut.text = ""
        self.ids.rut_verificador.text = ""
        
        self.ids.nombres.text = ""
        self.ids.apellidos.text = ""
        self.ids.telefono.text = ""
        self.ids.celular.text = ""
        self.ids.correo.text = ""
        
    def accion_boton(self, args):
        
        if args.icon == "exit-run":
            self.siguiente()
            
        if args.icon == "delete":
            self.formatear()
        
        if args.icon == "pencil":
            
            if len(self.ids.nombres.text) >= 3 and len(self.ids.apellidos.text) >= 3  and len(self.ids.celular.text) >= 9 and "@" in self.ids.correo.text:
                if len(self.ids.rut.text) >= 8:
                    if self.ids.rut_verificador.text.lower() in "123456789k":
                        rut = self.ids.rut.text+"-"+self.ids.rut_verificador.text
                        if len(self.ids.telefono) >= 7:
                            pass
                            
                    else:
                        noti = Notificacion("Error", "El Verificador debe tener uno de estos verificadores 123456789k")
                        noti.open()
                else:
                    noti = Notificacion("Error", "El rut debe tener 8 caracteres")
                    noti.open()
                
            else:
                noti = Notificacion("Error", "Error todos los campos tienen que estar correcto")
                noti.open()  

            