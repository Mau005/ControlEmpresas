from entidades.registrarlocales import RegistrarLocales
from entidades.registro_notas_empresas import Registro_Notas_Empresas
from entidades.registroempresas import RegistroEmpresas
from entidades.registrardepartamento import RegistrarDepartamento
from entidades.registroproductos import RegistroProductos
from entidades.registroservicio import RegistroServicios
from entidades.registroserviciosdiarios import RegistroServiciosDiarios
from core.herramientas import Herramientas as her


class Querys():

    def __init__(self, bd):
        self.bd = bd

    def existe_usuario(self, nombre_cuenta):
        querys = f'SELECT * FROM cuentas WHERE nombre_cuenta = "{nombre_cuenta}";'
        return self.bd.consultar(querys)

    def registrar_cuenta(self, nombre_usuario, contraseña):
        querys = f'INSERT INTO cuentas(nombre_cuenta, contraseña) VALUES("{nombre_usuario}", SHA("{contraseña}"));'
        return self.bd.insertar(querys)

    def consultar_cuenta(self, usuario, contraseña):
        querys = f'SELECT * FROM cuentas WHERE nombre_cuenta = "{usuario}" AND contraseña = "{contraseña}";'
        datos = self.bd.consultar(querys)
        return datos

    def actualizar_grupo_usuario(self, correo, grupo):
        querys = f'UPDATE USUARIOS SET GRUPOS = {grupo} WHERE CORREO = "{correo}";'
        return self.bd.insertar(querys)



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
        objeto = her.recuperacion_sentencia(objeto)
        empresa = RegistroEmpresas()
        empresa.__dict__ = objeto.__dict__

        print(empresa)
        querys = '''
        INSERT INTO EMPRESAS(rut_empresa, nombre_empresa, giro_empresa, direccion_empresa, correo_empresa, 
        correo_respaldo, telefono_empresa, celular_empresa)
        VALUES({}, {}, {}, {}, {}, {}, {}, {});
        '''.format(empresa.rut_empresa, empresa.nombre_empresa, empresa.giro_empresa, empresa.direccion_empresa, empresa.correo_empresa,
                   empresa.correo_respaldo, empresa.telefono_empresa, empresa.celular_empresa)
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

    def solicitar_listado_servicios(self):
        querys = f'SELECT ID_SERVICIO, NOMBRE_SERVICIO FROM SERVICIOS;'
        return self.bd.consultar(querys, all=True)

    def registrar_productos(self, objeto):
        objeto = her.recuperacion_sentencia(objeto)
        productos = RegistroProductos()
        productos.__dict__ = objeto.__dict__

        print(f"Productos: {productos}")
        querys = '''
        INSERT INTO productos(nombre_producto, descripcion, cantidad, id_local)
        VALUES({}, {}, {}, {});
        '''.format(productos.nombre_producto, productos.descripcion, productos.cantidad, productos.id_local)
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
        querys = "SELECT id_local, nombre_local	FROM locales;"
        return self.bd.consultar(querys, all=True)

    def registrar_trabajador(self, rut, id_local, sueldo, dia_pago):
        querys = '''
        INSERT INTO trabajadores(RUT, ID_LOCAL, SUELDO, DIA_PAGO)
        VALUES("{}", {}, {}, {});
        '''.format(rut, id_local, sueldo, dia_pago)
        return self.bd.insertar(querys)

    def registrar_locales(self, objeto):
        objeto = her.recuperacion_sentencia(objeto)
        local = RegistrarLocales()
        local.__dict__ = objeto.__dict__

        querys = '''
        INSERT INTO locales(nombre_local, telefono_local, direccion)
        VALUES({}, {}, {})
        '''.format(local.nombre_local, local.telefono_local, local.direccion)
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

    def listado_notas_empresa_especifica(self, contenido):
        querys = """
        SELECT * FROM registro_notas_empresas
        WHERE RUT_EMPRESA = '{}'
        GROUP BY FECHA_CREACION DESC;
        """.format(contenido)
        datos = self.bd.consultar(querys, all=True)
        lista_notas = []
        for nota in datos.get("datos"):
            lista_notas.append(Registro_Notas_Empresas(id_registro=nota[0], notas=nota[1],
                                                       rut_empresa=nota[2], correo=nota[3],
                                                       fecha_creacion=nota[4]))
        datos.update({"datos": lista_notas})
        return datos

    def registrar_departamento(self, objeto):
        objeto = her.recuperacion_sentencia(objeto)
        obj = RegistrarDepartamento()
        obj.__dict__ = objeto.__dict__
        querys = """
        INSERT INTO departamentos (nombre_grupo, descripcion, id_local) 
        VALUES ({}, {}, {});
        """.format(obj.nombre_departamento, obj.descripcion, obj.id_local)
        return self.bd.insertar(querys)

    def asignar_grupo(self, rut_Trabajador, id_grupo):
        querys = """
        INSERT INTO grupos_trabajadores(ID_GRUPO, RUT_TRABAJADOR) 
        VALUES ('{}', '{}')
        """.format(id_grupo, rut_Trabajador)
        return self.bd.insertar(querys)
