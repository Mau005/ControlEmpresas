
import smtplib
import ssl
from email.mime.text import MIMEText

class EstructurasCorreos():
    contador = 0

    @classmethod
    def __contador(cls):
        cls.contador += 1

    def __init__(self, correo_sistema, correo_destino, titulo):
        self.__contador()
        self.idMensaje = self.contador
        self.correo_sistema = correo_sistema
        self.correo_destino = correo_destino
        self.titulo = titulo
        self.estado = False

    def preparar_envio(self, msj):
        mensaje = MIMEText(msj)
        mensaje['From'] = self.correo_sistema
        mensaje['To'] = self.correo_destino
        mensaje['Subject'] = self.titulo
        return mensaje

class Servicio_Correos():
    def __init__(self, correo_sistema, contraseña, host, port):
        self.enMovimiento = True
        self.__pendientes = {}

        self.correo_sistema = correo_sistema
        self.correo_destino = ""
        self.__contrasenia = contraseña
        self.__host = host
        self.__port = port
        self.__mail_server = self.__preparar_servidor()


    def __preparar_servidor(self):
        """
        Methodo que retorna un servidor completo
        :return:
        """
        contexto = ssl.create_default_context()
        mail_server = smtplib.SMTP_SSL(host = self.__host, port = self.__port, context=contexto)
        mail_server.login(self.correo_sistema, self.__contrasenia)
        return mail_server

    def enviar_mensaje(self, correo_destino, mensaje):
        objeto = EstructurasCorreos(self.correo_sistema, correo_destino, "Un Titulo rapido")
        self.__mail_server.sendmail(self.correo_sistema, correo_destino, objeto.preparar_envio(mensaje).as_string())

if __name__ == "__main__":
    mensaje = """
    Bienvenido {}.
        A la aplicacion {} Espero que te sientas bien
        o si no cambia la cilla para sentarte mejor
        
        atte
        Tu Hermana.
    """.format("by_ricky008", "el_secuestra_papitas")
    email = Servicio_Correos("no-reply@lostrespinos.cl", "4Rw&)E--", "mail.lostrespinos.cl", 465)


    for x in range(1, 20):
        email.enviar_mensaje("mpino1701@gmail.com", mensaje)

