import sys

from kivy.logger import Logger
from kivy.properties import ObjectProperty

from core.constantes import PROTOCOLOERROR
from core.herramientas import Herramientas as her
from ventanas.widgets_predefinidos import MDScreenAbstrac, NotificacionText
from ventanas.widgets_predefinidos import Notificacion


class Entrada(MDScreenAbstrac):
    entrada_usuario = ObjectProperty()
    pass_usuario = ObjectProperty()
    botones = ObjectProperty()

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.contenido_usuario = her.cargar_json("data/ConfiguracionCliente.json", "Se carga configuración del cliente")
        Logger.info("Se Cargado la configuración")
        self.botones.data = {"Configuración": "ip-network",
                             "Recuperar Cuenta": "account-box",
                             "Salir": "exit-run"}
        self.noti_network = NotificacionText("Configura la IP", "127.0.0.1", aceptar=self.func_concurrente_notificacion)

        self.noti_recuperacion = NotificacionText("Indique correo electronico: ", "ejemplo@tudominio.cl",
                                                  aceptar=self.func_concurrente_recuperacion)

        self.noti_recuperacion_digito = NotificacionText("Recuperacion", "Indicame el Codigo",
                                                         aceptar=self.func_concurrente_recuperacion_digito)

        if self.contenido_usuario["Usuario"]["boton"]:
            self.entrada_usuario.text = self.contenido_usuario["Usuario"]["correo"]
            self.pass_usuario.text = self.contenido_usuario["Usuario"]["contraseña"]

        self.ids.usuario_guardar.active = self.contenido_usuario["Usuario"]["boton"]

    def func_concurrente_notificacion(self, *args):
        self.network.ip = self.noti_network.campo.text
        self.network.iniciar()

    def func_concurrente_recuperacion(self, *args):
        self.network.enviar({"estado": "recuperacion", "contenido": self.noti_recuperacion.campo.text})
        info = self.network.recibir()

        noti = Notificacion("Recuperación",
                            "Se ha enviado un correo electornico con el numero verificador, por faro inicie seccion y "
                            "complete los datos")
        noti.open()

    def accion_boton(self, arg):
        print(arg.icon)
        if arg.icon == "exit-run":
            sys.exit()
        if arg.icon == "ip-network":
            self.noti_network.open()
        if arg.icon == "account-box":
            self.noti_recuperacion.open()
            # self.manager.current = "recuperacion"

    def guardado(self, correo, contraseña, boton, condicion=False):
        self.contenido_usuario["Usuario"]["contraseña"] = contraseña
        self.contenido_usuario["Usuario"]["correo"] = correo
        self.contenido_usuario["Usuario"]["boton"] = boton
        if condicion:
            self.entrada_usuario.text = correo
            self.pass_usuario.text = contraseña

        her.escribir_json(self.contenido_usuario, "data/ConfiguracionCliente.json")

    def func_concurrente_recuperacion_digito(self, *args):

        self.network.enviar({"estado": "recuperacion_digito", "contenido": self.noti_recuperacion_digito.campo.text})
        info = self.network.recibir()
        print(f"Contenido descargado es: {info}")

        if info.get("estado"):
            noti = Notificacion("Aceptado", "Se confirma el digito")
            noti.open()
            self.manager.current = "recuperacion"
            self.manager.get_screen("recuperacion").activar()
        else:
            noti = Notificacion("Error", "Digito incorrecto")
            noti.open()

    def ingresar_usuario(self, correo, password):
        if self.ids.usuario_guardar.active:
            if not (self.contenido_usuario["Usuario"]["contraseña"] == password):
                password = her.cifrado_sha1(password)
                self.guardado(self.entrada_usuario.text, password, self.ids.usuario_guardar.active)

        else:
            self.guardado("", "", False, condicion=True)
            password = her.cifrado_sha1(password)

        noti = Notificacion("Error", "")
        if len(correo) >= 2 and len(password) >= 2:
            estructura = {"estado": "login", "correo": correo, "password": password}
            self.network.enviar(estructura)
            info = self.network.recibir()
            print(f"login info: {info}")
            if info.get("estado"):
                noti.title = f"Bienvenido {correo}"
                noti.text = info.get("MOTD")
                self.siguiente()
                noti.open()
            else:
                condicion = info.get("condicion")
                if condicion == "recuperacion":
                    self.noti_recuperacion_digito.open()

                elif condicion == "NETWORK":
                    notilocal = Notificacion("Error", PROTOCOLOERROR[
                        info.get("condicion")] + " Desea intentar conectarse Nuevamente? ",
                                             funcion_concurrente=self.network.iniciar)
                    notilocal.open()
                else:
                    noti = Notificacion("Error", "Usuario o Contraseña incorrecta")
                    noti.open()

        else:
            noti = Notificacion("ror", "Tiene que ser mas de 2 caracteres en usaurio o passwordEr")
            noti.open()

    def actualizar(self, dt):
        return super().actualizar(dt)

    def siguiente(self, *dt):
        return super().siguiente(*dt)

    def volver(self, *dt):
        return super().volver(*dt)
