from core.constantes import TIEMPOESPERADIGITO
from core.herramientas import Herramientas as her


class RecuperacionCuenta():
    """
    Clase orientada a gestionar el control de recuperacion de
    cuentas de usuario
    """

    def __init__(self, servicio_correos, control_network):
        self.correo = None
        self.digito = None
        self.activo = False
        self.tiempo_recuperacion = TIEMPOESPERADIGITO
        self.tiempo_transcurrido = 0
        self.intentos = 0
        self.servicio_correos = servicio_correos
        self.control_network = control_network

    def iniciar(self, correo, digito):
        """
        Iniciamos los procesos de recuperacion
        :param correo:  correo de usuario
        :param digito:  digito verificador para gestionar el cambio
        :return: True
        """
        self.correo = correo
        self.digito = digito
        mensaje = her.cargar_archivo("data/correos/Recuperacion_Cuenta.msg", "Se cargo mensaje correo")
        digito = her.numero_aleatorio()
        self.servicio_correos.enviar_mensaje(self.correo, mensaje.format(self.correo, digito))
        return True

    def actualizar(self):
        """
        Actualizara el tiempo cada segundo
        :return:
        """
        if self.tiempo_recuperacion is not None:
            self.tiempo_transcurrido += 1
