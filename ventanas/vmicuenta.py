from entidades.cuentas import Cuentas
from ventanas.widgets_predefinidos import MDScreenAbstrac


class VMiCuenta(MDScreenAbstrac):

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.cuenta = None

    def formatear(self, *args):
        self.ids.nombre_cuenta.text = ""
        self.ids.contra = ""
        self.ids.contra2 = ""

    def set_cuenta(self, cuenta: Cuentas):
        self.cuenta = cuenta

    def activar(self):
        super().activar()

    def siguiente(self, *dt):
        return super().siguiente(*dt)

    def actualizar(self, *dt):
        return super().actualizar(*dt)

    def volver(self, *dt):
        return super().volver(*dt)
