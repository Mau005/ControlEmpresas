from ventanas.widgets_predefinidos import MDScreenAbstrac, Notificacion
from kivymd.uix.pickers import MDDatePicker
from kivy.properties import ObjectProperty
from entidades.registroservicio import RegistroServicios
from core.constantes import BUTTONCREATE


class VServicios(MDScreenAbstrac):
    nombre = ObjectProperty()
    descr = ObjectProperty()
    id_estado = ObjectProperty()
    precio = ObjectProperty()
    botones_servicios = ObjectProperty()

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.set_activo(True)
        self.data = BUTTONCREATE
        self.fecha_inicio = None
        self.fecha_termino = None
        self.botones_servicios.data = self.data
        self.correo = "prueba"

    def accion_boton(self, arg):
        print(arg.icon)
        if arg.icon == "delete":
            self.formatear()
        if arg.icon == "exit-run":
            self.botones_servicios.on_close()
            self.siguiente()
        if arg.icon == "pencil":
            if self.fecha_inicio is None:
                noti = Notificacion("ERROR", "Alemenos debe indicar la fecha de inicio.")
                noti.open()
            else:
                if self.fecha_termino is None:
                    self.fecha_termino = "NULL"
                obj = RegistroServicios(nombre=self.nombre.text,
                                        descr=self.descr.text,
                                        fecha_inicio=str(self.fecha_inicio),
                                        fecha_termino=str(self.fecha_termino),
                                        correo=self.correo,
                                        id_estado=self.id_estado.text,
                                        precio=self.precio.text
                                        )
                self.network.enviar(obj.preparar())
                datos = self.network.recibir()
                if datos.get("estado"):
                    test = Notificacion("Exito", datos.get("condicion"))
                    test.open()
                    self.formatear()
                else:
                    test = Notificacion("Error", datos.get("condicion"))
                    test.open()

    def formatear(self):
        self.fecha_termino = None
        self.fecha_termino = None
        self.nombre.text = ""
        self.id_estado.text = ""
        self.descr.text = ""
        self.precio.text = ""
        self.ids.btn_fecha.text = "00/00/00 al 00/00/00"

    def abrir_fecha(self):
        date_dialog = MDDatePicker(mode="range")
        date_dialog.bind(on_cancel=self.on_cancel, on_save=self.on_save)
        date_dialog.open()

    def on_cancel(self, instance, value):
        """Events called when the "CANCEL" dialog box button is clicked."""

    def on_save(self, instance, value, date_range):
        if len(date_range) >= 2:
            self.fecha_inicio = date_range[0]
            self.fecha_termino = date_range[-1]
            formato = f"{self.fecha_inicio} al {self.fecha_termino}"
            self.ids.btn_fecha.text = str(formato)
        else:
            self.fecha_inicio = value
            self.fecha_termino = None
            self.ids.btn_fecha.text = str(value)

    def actualizar(self, *dt):
        return super().actualizar(*dt)

    def siguiente(self, *dt):
        return super().siguiente(*dt)

    def volver(self, *dt):
        return super().volver(*dt)
