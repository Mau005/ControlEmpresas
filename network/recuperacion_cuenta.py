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
        self.tiempo_recuperacion = None
        self.tiempo_transcurrido = 0
        self.intentos = 0
        self.servicio_correos = servicio_correos
        self.control_network = control_network
        self.tiempo_recuperacion = 60 * her.cargar_json("data/ConfiguracionServidor.json")["Servidor"]["TIEMPOESPERADIGITO"]

    def iniciar(self, correo):
        """
        Iniciamos los procesos de recuperacion
        :param correo:  correo de usuario
        :return: True
        """
        self.correo = correo
        self.digito = str(her.numero_aleatorio())
        mensaje = her.cargar_archivo("data/correos/Recuperacion_Cuenta.msg", "Se cargo mensaje correo")
        self.servicio_correos.enviar_mensaje(self.correo, "kastachana: Recuperación de Cuenta", mensaje.format(self.correo, self.digito))
        self.control_network.agregar_control_recuperacion(self.correo, self.digito)

    def actualizar(self):
        """
        Actualizara el tiempo cada segundo
        :return:
        """
        if self.tiempo_recuperacion is not None:
            self.tiempo_transcurrido += 1
            if self.tiempo_transcurrido >= self.tiempo_recuperacion:
                print("se ha superado el maximo de tiempo permitido para poder realizar la gestion de recuperacion")
