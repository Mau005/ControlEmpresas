from entidades.registrardepartamento import RegistrarDepartamento
from ventanas.widgets_predefinidos import MDScreenAbstrac, Notificacion, MenuEntidades
from kivy.properties import ObjectProperty
from core.constantes import PROTOCOLOERROR
from kivy.logger import Logger


class VDepartamentos(MDScreenAbstrac):

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.coleccion_locales = MenuEntidades(self.network, "Local:", "Local:", self.ids.menu_local, filtro="int")

    def crear(self, *args):
        if len(self.ids.nombre_grupo.text) <= 5:
            noti = Notificacion("Error", "Nombre de grupo almenos debe tener 5 caracteres\n")
            noti.open()
            return
        if self.ids.menu_local.text == "Local:":
            noti = Notificacion("Error", "Tiene que seleccionar algun local\n")
            noti.open()
            return

        objeto = RegistrarDepartamento(
            nombre_departamento=self.ids.nombre_grupo.text,
            descripcion=self.ids.desc_grupo.text,
            id_local=self.coleccion_locales.dato_guardar
        )
        self.network.enviar(objeto.preparar())
        info = self.network.recibir()
        if info.get("estado"):
            self.formatear()
            noti = Notificacion("Exito", f"Se ha registrado el grupo: {objeto.nombre_departamento}")
            noti.open()
            return None
        noti = Notificacion("Error", PROTOCOLOERROR[info.get("condicion")])
        noti.open()
        Logger.critical(f"Error no contralado en VGrupos datos: {info}")

    def formatear(self):
        self.ids.nombre_grupo.text = ""
        self.ids.desc_grupo.text = ""
        self.ids.menu_local.text = "Local:"
        self.coleccion_locales.dato_guardar = None

    def activar(self):
        self.coleccion_locales.generar_consulta("menu_locales")
        super().activar()

    def siguiente(self, *dt):
        return super().siguiente(*dt)

    def actualizar(self, *dt):
        return super().actualizar(*dt)

    def volver(self, *dt):
        return super().volver(*dt)
