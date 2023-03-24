import sys
from kivy.properties import ObjectProperty

from core.constantes import PROTOCOLOERROR, CONFIGURATION_WARNING
from core.herramientas import Herramientas as her
from entidades.cuentas import Cuentas
from ventanas.widgets_predefinidos import MDScreenAbstrac, NotificacionText
from ventanas.widgets_predefinidos import Notificacion


class Entrada(MDScreenAbstrac):
    entrada_usuario = ObjectProperty()
    pass_usuario = ObjectProperty()

    def __init__(self, network, manejador, nombre, siguiente=None, volver=None, **kw):
        super().__init__(network, manejador, nombre, siguiente, volver, **kw)
        self.contenido_usuario = her.cargar_json("data/ConfiguracionCliente.json")
        if self.contenido_usuario is None:
            self.contenido_usuario = CONFIGURATION_WARNING
        self.noti_network = NotificacionText("Configuración de IP y Puerto", "Ejemplo: 127.0.0.1:7171",
                                             aceptar=self.func_concurrente_notificacion)

        self.noti_recuperacion = NotificacionText("Indique correo electronico: ", "ejemplo@tudominio.cl",
                                                  aceptar=self.func_concurrente_recuperacion)

        self.noti_recuperacion_digito = NotificacionText("Recuperacion", "Indicame el Codigo",
                                                         aceptar=self.func_concurrente_recuperacion_digito)

        if self.contenido_usuario["Usuario"]["boton"]:
            self.entrada_usuario.text = self.contenido_usuario["Usuario"]["correo"]
            self.pass_usuario.text = self.contenido_usuario["Usuario"]["contraseña"]

        self.ids.usuario_guardar.active = self.contenido_usuario["Usuario"]["boton"]

    def func_concurrente_notificacion(self, args):
        ip, puerto = self.noti_network.campo.text.split(":")
        print(f"Ip: {ip} Port: {puerto}")
        try:
            self.network.ip = ip
            self.network.port = int(puerto)
            self.network.iniciar()
        except ValueError:
            noti = Notificacion("Error en puerto", "El puerto solo debe tener numeros no letras")
            noti.open()

    def func_concurrente_recuperacion(self, args):
        self.network.enviar({"estado": "recuperacion", "contenido": self.noti_recuperacion.campo.text})
        self.network.recibir()
        noti = Notificacion("Recuperación",
                            "Se ha enviado un correo electornico con el numero verificador, por faro inicie seccion y "
                            "complete los datos")
        noti.open()

    def accion_boton(self, arg):
        if arg == "salir":
            sys.exit()
        if arg == "configurar ip":
            self.noti_network.open()
        if arg == "recuperar":
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

    def ingresar_usuario(self, nombre_usuario, password):
        if self.ids.usuario_guardar.active:
            if not (self.contenido_usuario["Usuario"]["contraseña"] == password):
                password = her.cifrado_sha1(password)
                self.guardado(self.entrada_usuario.text, password, self.ids.usuario_guardar.active)
        else:
            self.guardado("", "", False, condicion=True)
            password = her.cifrado_sha1(password)

        if not len(nombre_usuario) >= 2 and not len(password) >= 2:
            noti = Notificacion("Error", "La casilla de Nombre de usuario y contraseña debe tener contenido")
            noti.open()
            return None

        cuenta = Cuentas(
            nombre_cuenta=nombre_usuario,
            contraseña=password
        )
        cuenta = cuenta.preparar()
        cuenta.update({"estado":"login"})# proceso se salta la creacion de un objeto de tipo cuenta
        self.network.enviar(cuenta)
        info = self.network.recibir()
        if info.get("estado"):
            noti = Notificacion(f"Bienvenido {nombre_usuario}", info.get("MOTD"))
            self.siguiente()
            noti.open()
            return None

        condicion = info.get("condicion")

        if condicion == "recuperacion":
            self.noti_recuperacion_digito.open()
            return
        elif condicion == "NETWORK":  # condicion local
            noti = Notificacion("Error", PROTOCOLOERROR[
                info.get("condicion")] + " Desea intentar conectarse Nuevamente? ",
                                funcion_concurrente=self.network.iniciar)
            noti.open()
            return
        else:
            noti = Notificacion("Error", PROTOCOLOERROR[condicion])
            noti.open()
            return

    def actualizar(self, dt):
        return super().actualizar(dt)

    def siguiente(self, *dt):
        return super().siguiente(*dt)

    def volver(self, *dt):
        return super().volver(*dt)
