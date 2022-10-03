from ventanas.widgets_predefinidos import MDScreenAbstrac, MenuEntidades, Notificacion
from core.constantes import BUTTONCREATE
from entidades.registro_notas_empresas import Registro_Notas_Empresas
class VNotasEmpresas(MDScreenAbstrac):

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.ids.botones.data = BUTTONCREATE
        self.coleccion_empresas = MenuEntidades(self.network, "Rut Empresa:", "Rut:", self.ids.boton_empresas)

    def accion_boton(self, arg):

        if arg.icon == "pencil":
            objeto = Registro_Notas_Empresas(
                rut_empresa = self.coleccion_empresas.dato_guardar,
                notas = self.ids.nota_empresas.text
            )

            self.network.enviar(objeto.preparar())
            info = self.network.recibir()
            if info.get("estado"):
                noti = Notificacion("Exito", f"Se ha registrado una nota  a la empresa: {self.coleccion_empresas.dato_guardar}")
                noti.open()
                return
            if info.get("condicion") == "privilegios":
                noti = Notificacion("Error",
                                    f"No tienes los privilegios necesarios para crear una nota de empresa")
                noti.open()
                return
            noti = Notificacion("Error",
                                f"Hubo un error donde no se pudo controlar: {info}")
            noti.open()
            print("error en vnotasempresas proceso de recibir información")
            return




        if arg.icon == "delete":
            self.formatear()

        if arg.icon == "exit-run":
            self.siguiente()
            self.formatear()

    def activar(self):
        self.coleccion_empresas.generar_consulta("menu_empresas")
        super().activar()

    def formatear(self):
        self.ids.boton_empresas.text = "Rut Empresa:"
        self.ids.nota_empresas.text = ""
        self.coleccion_empresas.dato_guardar = None

    def siguiente(self, *dt):
        return super().siguiente(*dt)

    def volver(self, *dt):
        return super().volver(*dt)

    def actualizar(self, *dt):
        return super().actualizar(*dt)
