from core.constantes import PROTOCOLOERROR
from ventanas.empresa import Empresa
from ventanas.widgets_predefinidos import MDScreenAbstrac, Notificacion
from entidades.registroempresas import RegistroEmpresas
from core.herramientas import Herramientas as her
from kivy.logger import Logger


class VEmpresas(MDScreenAbstrac):
    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.correo = "prueba"
        self.empresa = Empresa()
        self.ids.contenedor_principal.add_widget(self.empresa)

    def crear(self, *args):
        if not self.empresa.crear():
            return

        verificando_rut = her.verificar_rut(self.empresa.rut_empresa.text)
        if not verificando_rut[0]:
            noti = Notificacion("Error", verificando_rut[1])
            noti.open()
            return

        objeto = self.empresa.generar_objeto(verificando_rut[1])

        self.network.enviar(objeto.preparar())
        info = self.network.recibir()

        if info.get("estado"):
            noti = Notificacion("Exito", f"Se ha generado con exito la Empresa {objeto.nombre_empresa}")
            noti.open()
            self.formatear()
            return None

        noti = Notificacion("Error", PROTOCOLOERROR[info.get("condicion")])
        noti.open()
        return None

    def formatear(self, *args):
        self.empresa.formatear()

    def actualizar(self, *dt):
        return super().actualizar(*dt)

    def siguiente(self, *dt):
        self.formatear()
        return super().siguiente(*dt)

    def volver(self, *dt):
        return super().volver(*dt)
