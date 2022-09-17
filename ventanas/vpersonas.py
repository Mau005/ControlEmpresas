from entidades.registropersonas import RegistroPersonas
from ventanas.widgets_predefinidos import MDScreenAbstrac, Notificacion
from kivy.properties import ObjectProperty
from core.herramientas import Herramientas as her
from kivy.logger import Logger


class VPersonas(MDScreenAbstrac):
    botones = ObjectProperty()

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.data = {
            'Crear': 'pencil',
            'Formatear': 'delete',
            'Salir': 'exit-run',
        }
        self.botones.data = self.data

    def formatear(self):
        self.ids.rut.text = ""
        self.ids.nombres.text = ""
        self.ids.apellidos.text = ""
        self.ids.telefono.text = ""
        self.ids.celular.text = ""
        self.ids.correo_sistema.text = ""

    def accion_boton(self, args):

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
                                          correo=self.ids.correo_sistema.text)
                self.network.enviar(objeto.preparar())
                print(objeto)
                info = self.network.recibir()
                if info.get("estado"):
                    Logger.info("se ha registrado el usuario correctamente")
                    noti.title = "Exito"
                    noti.text = "Usuario ingresado correctamente"
                    self.formatear()
                    self.siguiente()
                else:
                    Logger.warning("No se ha podido registrar el usuario")
                    noti.text = "No se ha podido registrar este usuario, el rut ya existe"
            noti.open()
