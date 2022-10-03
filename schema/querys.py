from entidades.registroservicio import RegistroServicios
from entidades.registroserviciosdiarios import RegistroServiciosDiarios
from core.herramientas import Herramientas as her


class Querys():

    def __init__(self, bd):
        self.bd = bd

    def existe_usuario(self, correo):
        querys = f'SELECT * FROM USUARIOS WHERE CORREO = "{correo}";'
        return self.bd.consultar(querys)

    def consultar_usuario(self, correo, contraseña):
        querys = f'SELECT * FROM USUARIOS WHERE CORREO = "{correo}" AND CONTRASEÑA = "{contraseña}";'
        datos = self.bd.consultar(querys)
        return datos

    def actualizar_grupo_usuario(self, correo, grupo):
        querys = f'UPDATE USUARIOS SET GRUPOS = {grupo} WHERE CORREO = "{correo}";'
        return self.bd.insertar(querys)

    def registrar_usuario(self, correo, contraseña):
        querys = f'INSERT INTO USUARIOS(CORREO,CONTRASEÑA) VALUES("{correo}", SHA({contraseña}));'
        return self.bd.insertar(querys)  # retorna usuario existente un dic

    def solicitar_estados(self):
        querys = f'SELECT * FROM ESTADOS;'
        return self.bd.consultar(querys, all=True)

    def registrar_baneo(self, correo, ip, descr=""):
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

    def registrar_servicios(self, datos):
        objeto = RegistroServicios()
        objeto.__dict__ = her.recuperacion_sentencia(datos).__dict__
        print(objeto)
        querys = f'''
        INSERT INTO SERVICIOS(NOMBRE_SERVICIO, DESCRIPCION, FECHA_INICIO, FECHA_TERMINO, 
        ID_ESTADO, RUT_TRABAJADOR, RUT_PERSONA)
        VALUES({objeto.nombre}, {objeto.descr}, {objeto.fecha_inicio}, {objeto.fecha_termino},
        {objeto.id_estado}, {objeto.rut_trabajador}, {objeto.rut_persona})
        '''
        print(querys)

        return self.bd.insertar(querys)

    def registrar_empresas(self, objeto):

        querys = '''
        INSERT INTO EMPRESAS(RUT_EMPRESA, NOMBRE_EMPRESA, GIRO_EMPRESA, DIRECCION, TELEFONO, CORREO_EMPRESA, CORREO_RESPALDO, CELULAR_EMPRESA)
        VALUES("{0}", "{1}", "{2}", "{3}", "{4}", "{5}" , "{6}", "{7}");
        '''.format(objeto.rut_empresa, objeto.nombre_empresa, objeto.giro_empresa,
                   objeto.direccion_empresa, objeto.telefono, objeto.correo_empresa, objeto.correo_respaldo,
                   objeto.celular_empresa)
        return self.bd.insertar(querys)

    def registrar_personas(self, rut_persona, nombres, apellidos, telefono, celular, correo, rut_empresa):
        """
        Methodo utilizado para que gestione la creacion de usuarios nuevos
        comprobare si el correo existe, si no existe lo creara con default de password
        """
        consulta_correo = self.consultar_correo_existente(correo)

        msj_error = {"estado": False, "condicion": "correo"}
        if consulta_correo.get("estado"):
            return msj_error

        registro_persona = self.registrar_usuario(correo, "12345")

        if not registro_persona.get("estado"):
            return msj_error

        querys = '''
        INSERT INTO PERSONAS(RUT, NOMBRES, APELLIDOS, TELEFONO, CELULAR, CORREO, RUT_EMPRESA)
        VALUES("{}", "{}", "{}" , "{}" , "{}" , "{}", "{}"); 
        '''.format(rut_persona, nombres, apellidos, telefono, celular, correo, rut_empresa)

        return self.bd.insertar(querys)

    # ID_REGISTRO	RUT_EMPRESA	CORREO	FECHA_CREACION
    def registrar_notas_empresas(self, nota, rut_empresa, correo):
        querys = '''
        INSERT INTO registro_notas_empresas(NOTA, RUT_EMPRESA, CORREO)
        VALUES("{}", "{}", "{}")
        '''.format(nota, rut_empresa, correo)
        return self.bd.insertar(querys)

    def solicitar_lista_empresas(self):
        querys = f'SELECT RUT_EMPRESA, NOMBRE_EMPRESA FROM EMPRESAS;'
        return self.bd.consultar(querys, all=True)

    def solicitar_listado_servicios(self):
        querys = f'SELECT ID_SERVICIO, NOMBRE_SERVICIO FROM SERVICIOS;'
        return self.bd.consultar(querys, all=True)

    def registrar_productos(self, nombre, descripcion, cantidad):
        querys = '''
        INSERT INTO PRODUCTOS(NOMBRE_PRODUCTO, DESCRIPCION, CANTIDAD)
        VALUES("{}", "{}", {});
        '''.format(nombre, descripcion, cantidad)
        return self.bd.insertar(querys)

    def nueva_contraseña(self, correo, contraseña_nueva):
        querys = f'UPDATE USUARIOS SET CONTRASEÑA = "{contraseña_nueva}" WHERE CORREO = "{correo}";'
        return self.bd.insertar(querys)

    def solicitar_lista_productos(self):
        querys = f'SELECT ID_PRODUCTO, NOMBRE_PRODUCTO, CANTIDAD FROM productos;'
        return self.bd.consultar(querys, all=True)

    def lista_menu_estados(self):
        querys = f'SELECT ID_ESTADO, NOMBRE FROM ESTADOS;'
        return self.bd.consultar(querys, all=True)

    def registrar_servicio_diario(self, objeto):
        obj = RegistroServiciosDiarios()
        obj.__dict__ = objeto.__dict__
        obj = her.recuperacion_sentencia(obj)
        querys = '''
        INSERT INTO serviciosdiarios(NOMBRE_SERVICIO, ID_ESTADO, PRECIO, FECHA_SEMANA, URL_POSICION, UBICACION,
        RUT_USUARIO, RUT_TRABAJADOR, DESCR, TODA_SEMANA, ID_PRODUCTO, CANTIDAD)
        VALUES({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});
        '''.format(obj.nombre_servicio, obj.id_estado, obj.precio, obj.fecha_semana, obj.url_posicion, obj.ubicacion,
                   obj.rut_usuario, obj.rut_trabajador, obj.descr, obj.toda_semana, obj.id_producto, obj.cantidad)
        print(querys)
        return self.bd.insertar(querys)

    def lista_empresas(self):
        querys = '''
        select RUT_EMPRESA, NOMBRE_EMPRESA  from empresas;
        '''
        return self.bd.consultar(querys, all=True)

    def consultar_correo_existente(self, correo):
        querys = f'select CORREO  from usuarios where CORREO = "{correo}";'
        return self.bd.consultar(querys)

    def lista_menu_personas(self):
        querys = "SELECT RUT, CONCAT(NOMBRES, ' ', APELLIDOS) as Nombres FROM personas;"
        return self.bd.consultar(querys, all=True)

    def lista_menu_locales(self):
        querys = "SELECT ID_LOCAL, NOMBRE_LOCAL	FROM locales;"
        return self.bd.consultar(querys, all=True)

    def registrar_trabajador(self, rut, id_local, sueldo, dia_pago):
        querys = '''
        INSERT INTO trabajadores(RUT, ID_LOCAL, SUELDO, DIA_PAGO)
        VALUES("{}", {}, {}, {});
        '''.format(rut, id_local, sueldo, dia_pago)
        return self.bd.insertar(querys)

    def registrar_locales(self, nombre, telefono, direccion):
        querys = '''
        INSERT INTO locales(NOMBRE_LOCAL, TELEFONO_LOCAL, DIRECCION)
        VALUES("{}","{}","{}")
        '''.format(nombre, telefono, direccion)
        return self.bd.insertar(querys)

    def lista_menu_trabajadores(self):
        querys = """
        SELECT t.RUT, CONCAT(p.NOMBRES, ' ', p.APELLIDOS) as Nombres
        FROM trabajadores t
        JOIN personas p ON p.RUT = t.RUT;
        """
        return self.bd.consultar(querys, all=True)

    def lista_menu_productos(self):
        querys = "SELECT ID_PRODUCTO, NOMBRE_PRODUCTO FROM productos;"
        return self.bd.consultar(querys, all=True)

    def lista_menu_empresas(self):
        querys = "SELECT RUT_EMPRESA, NOMBRE_EMPRESA FROM empresas;"
        return self.bd.consultar(querys, all=True)
