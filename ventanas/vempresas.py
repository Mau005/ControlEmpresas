from ventanas.widgets_predefinidos import MDScreenAbstrac, Notificacion
from core.constantes import BUTTONCREATE
from entidades.registroempresas import RegistroEmpresas
from core.herramientas import Herramientas as her
from kivy.logger import Logger


class VEmpresas(MDScreenAbstrac):

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.data = BUTTONCREATE
        self.ids.botones.data = self.data
        self.correo = "prueba"

    def accion_boton(self, arg):
        if arg.icon == "exit-run":
            self.siguiente()
        if arg.icon == "pencil":
            longitud = 1
            noti = Notificacion("Error", "")
            estado = True
            if not (len(self.ids.rut_empresa.text) == 10):
                noti.text += "Debe tener 10 caracteres el RUT de Empresa ejemplo xxxxxxxx-x\n"
                estado = False
            if not (len(self.ids.nombre_empresa.text) >= longitud):
                noti.text += "Debe tener Contenido el Nombre de Empresa\n"
                estado = False
            if not (len(self.ids.giro_empresa.text) >= longitud):
                noti.text += "Debe tener Contenido el Giro de la empresa\n"
                estado = False
            if not (len(self.ids.direccion_empresa.text) >= longitud):
                noti.text += "Debe tener contenido la direccion de la empresa\n"
                estado = False
            if not (len(self.ids.celular_empresa.text) >= 8):
                noti.text += "El celular de empresa debe tener almenos 8 numeros\n"
                estado = False
            if not ("@" in self.ids.correo_empresa.text):
                noti.text += "El Correo de la empresa debe tener almenos un @\n"
                estado = False
            if estado:
                vericando_rut = her.verificar_rut(self.ids.rut_empresa.text)

                if vericando_rut[0]:
                    objeto = RegistroEmpresas(
                        rut_empresa=self.ids.rut_empresa.text,
                        nombre_empresa=self.ids.nombre_empresa.text,
                        giro_empresa=self.ids.giro_empresa.text,
                        direccion_empresa=self.ids.direccion_empresa.text,
                        telefono=self.ids.telefono_empresa.text,
                        celular_empresa=self.ids.celular_empresa.text,
                        correo_empresa=self.ids.correo_empresa.text,
                        correo_respaldo=self.ids.correo_respaldo_empresa.text,
                    )
                    self.network.enviar(objeto.preparar())
                    info = self.network.recibir()
                    if info.get("estado"):
                        Logger.info("Se ha creado el dato empresa")
                        noti.title = "Exito"
                        noti.text = info.get("condicion")
                        self.formatear()
                        self.siguiente()
                    else:

                        Logger.warning("No se ha podido registrar la empresa")
                        noti.text = info.get("condicion")
            noti.open()

        if arg.icon == "delete":
            self.formatear()

    def formatear(self):
        self.ids.rut_empresa.text = ""
        self.ids.nombre_empresa.text = ""
        self.ids.giro_empresa.text = ""
        self.ids.direccion_empresa.text = ""
        self.ids.telefono_empresa.text = ""
        self.ids.celular_empresa.text = ""
        self.ids.correo_empresa.text = ""
        self.ids.correo_respaldo_empresa.text = ""

    def actualizar(self, *dt):
        return super().actualizar(*dt)

    def siguiente(self, *dt):
        return super().siguiente(*dt)

    def volver(self, *dt):
        return super().volver(*dt)
