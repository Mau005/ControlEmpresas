from kivymd.uix.bottomsheet import MDListBottomSheet

from entidades.registropersonas import RegistroPersonas
from ventanas.widgets_predefinidos import MDScreenAbstrac, Notificacion
from kivy.properties import ObjectProperty
from core.herramientas import Herramientas as her
from kivy.logger import Logger


class Contenedor_Rut():
    def __init__(self, rut_empresa, nombre):
        self.rut_empresa = rut_empresa
        self.nombre = nombre


class VPersonas(MDScreenAbstrac):
    botones = ObjectProperty()

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.data = {
            'Crear': 'pencil',
            'Formatear': 'delete',
            'Salir': 'exit-run',
        }
        self.lista_botones_empresas = {}
        self.botones.data = self.data
        self.seleccion_empresa = "Sin Empresa"
        self.correo_activo = False

    def buscar_empresas(self):
        bottom_sheet_menu = MDListBottomSheet()
        for nombre_key in self.lista_botones_empresas.keys():
            bottom_sheet_menu.add_item(f"{nombre_key}: {self.lista_botones_empresas.get(nombre_key).nombre}",
                                       self.callback_menu)
        bottom_sheet_menu.open()

    def callback_menu(self, arg):
        formato = arg.text.split(":")
        self.seleccion_empresa = formato[0]
        self.ids.boton_rut_empresas.text = f"Empresa: {formato[1]}"

    def activar(self):
        self.lista_botones_empresas.clear()
        self.network.enviar({"estado": "lista_empresas"})
        info = self.network.recibir()

        if info.get("estado"):
            for elementos in info.get("datos"):
                self.lista_botones_empresas.update({elementos[0]: Contenedor_Rut(elementos[0], elementos[1])})
                print(elementos)
        else:
            if info.get("condicion") == "privilegios":
                noti = Notificacion("Error", "No se ha podido cargar la lista de empresas dado que no tienes los "
                                             "privilegios "
                                             "correspondientes")
                noti.open()
        super().activar()

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
                                          correo=self.ids.correo_sistema.text,
                                          rut_empresa=self.seleccion_empresa)
                self.network.enviar(objeto.preparar())
                print(objeto)
                info = self.network.recibir()

                print(f"Datos que me envio el servidor: {info}")
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
