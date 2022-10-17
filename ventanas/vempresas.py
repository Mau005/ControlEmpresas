from ventanas.widgets_predefinidos import MDScreenAbstrac, Notificacion
from entidades.registroempresas import RegistroEmpresas
from core.herramientas import Herramientas as her
from kivy.logger import Logger


class VEmpresas(MDScreenAbstrac):

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.ids.botones_empresas.data = {'Crear': ["pencil", "on_release", self.crear],
                                          'Formatear': ["delete", "on_release", self.formatear],
                                          'Salir': ["exit-run", "on_release", self.siguiente]}
        self.correo = "prueba"

    def crear(self, *args):
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
        if not estado:
            noti.open()
            return None
        verificando_rut = her.verificar_rut(self.ids.rut_empresa.text)

        if verificando_rut[0]:
            objeto = RegistroEmpresas(
                rut_empresa=verificando_rut[1],
                nombre_empresa=self.ids.nombre_empresa.text,
                giro_empresa=self.ids.giro_empresa.text,
                direccion_empresa=self.ids.direccion_empresa.text,
                telefono_empresa=self.ids.telefono_empresa.text,
                celular_empresa=self.ids.celular_empresa.text,
                correo_empresa=self.ids.correo_empresa.text,
                correo_respaldo=self.ids.correo_respaldo_empresa.text,
            )
            self.network.enviar(objeto.preparar())
            info = self.network.recibir()
            if info.get("estado"):
                Logger.info("Se ha creado el dato empresa")
                noti = Notificacion("Exito", f"Se ha generado con exito la Empresa {objeto.nombre_empresa}")
                noti.open()
                self.formatear()
                self.siguiente()
                return None

            noti = Notificacion("Error", info.get("condicion"))
            noti.open()
            return None

    def accion_boton(self, arg):
        self.ids.botones_empresas.close_stack()

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
        self.formatear()
        return super().siguiente(*dt)

    def volver(self, *dt):
        return super().volver(*dt)
