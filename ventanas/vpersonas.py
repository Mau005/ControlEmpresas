from entidades.registropersonas import RegistroPersonas
from ventanas.widgets_predefinidos import MDScreenAbstrac, Notificacion, MenuEntidades
from kivy.properties import ObjectProperty
from core.herramientas import Herramientas as her
from core.constantes import BUTTONCREATE


class VPersonas(MDScreenAbstrac):
    botones = ObjectProperty()

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.data = BUTTONCREATE
        self.botones.data = self.data
        self.colecciones_empresas = MenuEntidades(self.network, "Empresa:", "Empresa:", self.ids.boton_rut_empresas)

    def activar(self):
        self.colecciones_empresas.generar_consulta("menu_empresas")
        super().activar()

    def formatear(self):
        self.ids.rut.text = ""
        self.ids.nombres.text = ""
        self.ids.apellidos.text = ""
        self.ids.telefono.text = ""
        self.ids.celular.text = ""
        self.ids.correo_sistema.text = ""
        self.ids.boton_rut_empresas.text = "Empresa:"
        self.colecciones_empresas.dato_guardar = None

    def accion_boton(self, args):
        self.botones.close_stack()
        if args.icon == "exit-run":
            self.siguiente()

        if args.icon == "delete":
            self.formatear()

        if args.icon == "pencil":
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
                    noti.text = "No se ha podido registrar este usuario, el rut ya existe o el correo ya se encuentra registrado"
            noti.open()

    def actualizar(self, dt):
        super().actualizar(dt)
