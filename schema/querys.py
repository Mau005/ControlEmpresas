

from distutils.debug import DEBUG
import sys


class Querys():
    
    def __init__(self, bd):
        self.bd = bd

        
    def consultar_usuario(self, correo, contraseña):
        querys = f'SELECT * FROM USUARIOS WHERE CORREO = "{correo}" AND CONTRASEÑA = SHA({contraseña});'
        datos = self.bd.consultar(querys)
        return datos
    
    def registrar_usuario(self, correo, contraseña):
        querys = f'INSERT INTO USUARIOS(CORREO,CONTRASEÑA) VALUES("{correo}", SHA({contraseña}));'
        condicion = self.bd.insertar(querys)
        
        if condicion["estado"]:
            return self.__registrar_accesos(correo)
        
        return condicion #retorna usuario existente un dic
    
    def __registrar_accesos(self, correo):
        querys = f'INSERT INTO ACCESOS(CORREO) VALUES("{correo}")'
        return self.bd.insertar(querys)
    
    def solicitar_estados(self):
        querys = f'SELECT * FROM ESTADOS;'
        return self.bd.consultar(querys, all= True)

    def registrar_baneo(self, correo, ip, descr = "" ):
        """Methodo de prueba dado que no se puede banear a un usuario por intento
        methodo deprecated

        Args:
            correo (str): correo
            ip (str): ip del cliente ingresado
            descr (str, optional): _description_. Defaults to "".

        Returns:
            _type_: _description_
        """
        querys = f'INSERT INTO HISTORIAL_BANEOS(CORREO,IP,DESCR) VALUES("{correo}", "{ip}", "{descr}")'
        return self.bd.insertar(querys)
        
    def registrar_servicios(self,datos):
        querys = f'''
        INSERT INTO SERVICIOS(NOMBRE_SERVICIO, DESCRIPCION, FECHA_INICIO, FECHA_TERMINO, PRECIO, ID_ESTADO)
        VALUES("{datos.get("nombre")}", "{datos.get("descr")}","{datos.get("fecha_inicio")}","{datos.get("fecha_termino")}", {int(datos.get("precio"))}, {int(datos.get("id_estado"))});
        '''
        
        return self.bd.insertar(querys)