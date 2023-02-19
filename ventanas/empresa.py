from kivymd.uix.boxlayout import MDBoxLayout

from entidades.registroempresas import RegistroEmpresas
from ventanas.widgets_predefinidos import Notificacion


class Empresa(MDBoxLayout):
    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.editar = False

    def generar_objeto(self, rut_verificado=None) -> RegistroEmpresas:
        return RegistroEmpresas(
            rut_empresa=rut_verificado if rut_verificado is not None else self.ids.rut_empresa.text,
            nombre_empresa=self.ids.nombre_empresa.text,
            giro_empresa=self.ids.giro_empresa.text,
            direccion_empresa=self.ids.direccion_empresa.text,
            telefono_empresa=self.ids.telefono_empresa.text,
            celular_empresa=self.ids.celular_empresa.text,
            correo_empresa=self.ids.correo_empresa.text,
            correo_respaldo=self.ids.correo_respaldo_empresa.text,
        )

    def activar(self, empresa: RegistroEmpresas, *args):
        if empresa is not None:
            self.editar = True
            self.ids.rut_empresa.max_text_length = 12
            self.ids.rut_empresa.text = empresa.rut_empresa
            self.ids.rut_empresa.disabled = True
            self.ids.nombre_empresa.text = empresa.nombre_empresa
            self.ids.giro_empresa.text = empresa.giro_empresa
            self.ids.direccion_empresa.text = empresa.direccion_empresa
            self.ids.telefono_empresa.text = empresa.telefono_empresa if empresa.telefono_empresa is not None else ""
            self.ids.celular_empresa.text = empresa.celular_empresa if empresa.celular_empresa is not None else ""
            self.ids.correo_empresa.text = empresa.correo_empresa
            self.ids.correo_respaldo_empresa.text = empresa.correo_respaldo if empresa.correo_respaldo is not None else ""
            return
        self.editar = False
        return

    def crear(self, *args):
        longitud = 1
        noti = Notificacion("Error", "")
        if not self.editar:
            if not (9 <= len(self.ids.rut_empresa.text) <= 10):
                noti.text += "Debe tener entre 9 y 10 caracteres el RUT de Empresa ejemplo xxxxxxxx-x\n"
        if not (len(self.ids.nombre_empresa.text) >= longitud):
            noti.text += "Debe tener Contenido el Nombre de Empresa\n"
        if not (len(self.ids.giro_empresa.text) >= longitud):
            noti.text += "Debe tener Contenido el Giro de la empresa\n"
        if not (len(self.ids.direccion_empresa.text) >= longitud):
            noti.text += "Debe tener contenido la direccion de la empresa\n"
        if not (len(self.ids.celular_empresa.text) >= 8):
            noti.text += "El celular de empresa debe tener almenos 8 numeros\n"
        if not ("@" in self.ids.correo_empresa.text):
            noti.text += "El Correo de la empresa debe tener almenos un @\n"
        if len(noti.text) >= 2:
            noti.open()
            return False
        return True

    def formatear(self, *args):
        self.editar = False
        self.ids.rut_empresa.text = ""
        self.ids.nombre_empresa.text = ""
        self.ids.giro_empresa.text = ""
        self.ids.direccion_empresa.text = ""
        self.ids.telefono_empresa.text = ""
        self.ids.celular_empresa.text = ""
        self.ids.correo_empresa.text = ""
        self.ids.correo_respaldo_empresa.text = ""
