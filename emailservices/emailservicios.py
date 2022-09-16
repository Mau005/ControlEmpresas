import smtplib
import ssl
from email.mime.text import MIMEText
from threading import Thread
import time
from core.constantes import REVISARCORREOS


class EstructurasCorreos:
    contador = 0

    def __init__(self, correo, correoUsuario, mensaje):
        self.__contador()
        self.idMensaje = self.contador
        self.correo = correo
        self.correoUsuario = correoUsuario
        self.mensaje = mensaje
        self.estado = False

    @classmethod
    def __contador(cls):
        cls.contador += 1


class EmailServicios(Thread):
    def __init__(self, correo, contrasenia, host, port):
        super(EmailServicios, self).__init__()
        self.__pendientes = {}
        self.correo = correo
        self.contrasenia = contrasenia
        self.host = host
        self.port = port
        self.enMovimiento = True
        self.__mailServer = self.__preparar_servidor()

    def __preparar_servidor(self):
        contexto = ssl.create_default_context()
        mailServer = smtplib.SMTP_SSL(self.host, self.port, context=contexto)
        mailServer.login(self.correo, self.contrasenia)
        return mailServer

    def __enviar_mensaje(self, correoUsuario, mensaje):
        self.__mailServer.sendmail(self.correo, correoUsuario, mensaje.as_string())

    def __pre_configuracion(self, msj, correoPropio, correoUsuario, titulo):
        mensaje = MIMEText(msj)
        mensaje['From'] = correoPropio
        mensaje['To'] = correoUsuario
        mensaje['Subject'] = titulo
        return mensaje

    def __cerrar(self):
        self.__mailServer.close()

    def enviar_bienvenida(self, correoUsuario):
        mensaje = self.__pre_configuracion(ME.TextEnviarBienvenida(correoUsuario), self.correo, correoUsuario,
                                           "Bienvenido a Kimn")
        objeto = EstructurasCorreos(self.correo, correoUsuario, mensaje)
        self.__pendientes.update({objeto.idMensaje: objeto})

    def enviar_codigo(self, correoUsuario, codigo):
        msj = ME.TextEnviarCodigo(correoUsuario, codigo)
        mensaje = self.__pre_configuracion(msj, self.correo, correoUsuario, "Codigo de Verificaciòn")
        objeto = EstructurasCorreos(self.correo, correoUsuario, mensaje)
        self.__pendientes.update({objeto.idMensaje: objeto})

    def __LimpiarMemoria(self, datos):
        for x in datos:
            self.__pendientes.pop(x)

    def run(self):
        print("[OK] Servicio de Email Activado")
        while self.enMovimiento:
            limpiar_memoria = []
            for elementos in self.__pendientes:
                print(elementos)
                if not self.__pendientes[elementos].estado:
                    self.__enviar_mensaje(self.__pendientes[elementos].correoUsuario,
                                          self.__pendientes[elementos].mensaje)
                    self.__pendientes[elementos].estado = True
                    limpiar_memoria.append(elementos)
            self.__LimpiarMemoria(limpiar_memoria)
            time.sleep(REVISARCORREOS)
        self.__cerrar()
