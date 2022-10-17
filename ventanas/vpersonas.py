from entidades.registropersonas import RegistroPersonas
from ventanas.widgets_predefinidos import MDScreenAbstrac, Notificacion, MenuEntidades
from core.herramientas import Herramientas as her
from core.constantes import PROTOCOLOERROR


class VPersonas(MDScreenAbstrac):

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.ids.botones_personas.data = {'Crear': ["pencil", "on_release", self.crear],
                                          'Formatear': ["delete", "on_release", self.formatear],
                                          'Salir': ["exit-run", "on_release", self.siguiente]}
        self.colecciones_empresas = MenuEntidades(self.network, "Empresa:", "Empresa:", self.ids.boton_rut_empresas)

    def crear(self, *args):
        noti = Notificacion("Error", "")
        estado = True
        if not len(self.ids.rut.text) == 10:
            noti.text += "El rut debe tener 10 caracteres ejemplo: 11222333-4\n"
            estado = False
        if not "@" in self.ids.correo_sistema.text:
            noti.text += "El Correo debe ser correcto ejemplo: tuempresa@tudominio.cl"
            estado = False

        rut_verificado = her.verificar_rut(self.ids.rut.text)

        if not rut_verificado[0]:
            estado = False
            noti.text += rut_verificado[1]

        if estado:
            objeto = RegistroPersonas(rut_persona=rut_verificado[1],
                                      nombres=self.ids.nombres.text,
                                      apellidos=self.ids.apellidos.text,
                                      telefono=self.ids.telefono.text,
                                      celular=self.ids.celular.text,
                                      correo=self.ids.correo_sistema.text,
                                      rut_empresa=self.colecciones_empresas.dato_guardar)
            self.network.enviar(objeto.preparar())
            info = self.network.recibir()
            if info.get("estado"):
                noti.title = "Exito"
                noti.text = "Usuario ingresado correctamente"
                self.formatear()
                self.siguiente()
            else:
                noti.text = PROTOCOLOERROR[info.get("condicion")]
        noti.open()

    def siguiente(self, *dt):
        self.formatear()
        super().siguiente(dt)

    def activar(self):
        self.colecciones_empresas.generar_consulta("menu_empresas")
        super().activar()

    def formatear(self, *args):
        self.ids.rut.text = ""
        self.ids.nombres.text = ""
        self.ids.apellidos.text = ""
        self.ids.telefono.text = ""
        self.ids.celular.text = ""
        self.ids.correo_sistema.text = ""
        self.ids.boton_rut_empresas.text = "Empresa:"
        self.colecciones_empresas.dato_guardar = None

    def accion_boton(self, args):
        self.ids.botones_personas.close_stack()

    def actualizar(self, dt):
        super().actualizar(dt)
