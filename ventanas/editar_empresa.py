from core.constantes import PROTOCOLOERROR
from entidades.registroempresas import RegistroEmpresas
from ventanas.empresa import Empresa
from ventanas.widgets_predefinidos import MDScreenAbstrac, Notificacion


class EditarEmpresa(MDScreenAbstrac):
    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.empresa = Empresa()
        self.ids.contenedor.add_widget(self.empresa)

    def activar(self, empresa: RegistroEmpresas, *args):
        self.empresa.activar(empresa)
        super().activar()

    def editar(self, *args):
        if not self.empresa.crear():
            return

        objeto = self.empresa.generar_objeto()
        self.network.enviar({"estado": "editar_empresa", "contenido": objeto})
        info = self.network.recibir()
        if info.get("estado"):
            noti = Notificacion("Exito", "Empresa se ha editado con exito")
            noti.open()
            self.empresa.formatear()
            self.siguiente()
            return

        noti = Notificacion("Error", PROTOCOLOERROR[info.get("condicion")])
        noti.open()
        return
