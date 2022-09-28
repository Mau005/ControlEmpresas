from core.herramientas import Herramientas as her


class Base_Correos():

    def __init__(self, servicio_correos):
        self.servicio_correos = servicio_correos

    def Correo_Bienvenida(self, nombre, correo, password):
        mensaje = her.cargar_archivo("data/correos/CreacionBienvenida.msg", "Creación Bienvenida")

        if mensaje != None:
            mensaje = mensaje.format(nombre, correo, password)
            self.servicio_correos.enviar_mensaje(correo, "Servicios Kastachana Correo de Bienvenida" ,mensaje)