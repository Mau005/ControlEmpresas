from entidades.registrarlocales import RegistrarLocales
from entidades.registronotas import RegistroNotas
from entidades.registroempresas import RegistroEmpresas
from entidades.registrardepartamento import RegistrarDepartamento
from entidades.registropersonas import RegistroPersonas
from entidades.registroproductos import RegistroProductos
from entidades.registroservicio import RegistroServicios
from entidades.registroserviciosdiarios import RegistroServiciosDiarios
from core.herramientas import Herramientas as her


class Querys():

    def __init__(self, bd):
        self.bd = bd

    def existe_cuenta(self, nombre_cuenta):
        """
        Methodo utilizado para gestionar si existe una cuenta
        """
        querys = f'SELECT nombre_cuenta FROM cuentas WHERE nombre_cuenta = "{nombre_cuenta}";'
        return self.bd.consultar(querys)

    def existe_persona(self, rut):
        """
        Methodo utilizado para gestionar si existe una persona
        """
        querys = f'SELECT rut_persona from personas WHERE rut_persona = "{rut}";'
        return self.bd.consultar(querys)

    def registrar_cuenta(self, nombre_cuenta, contraseña, acceso = 0):
        """
        Methodo utilizado para registrar una cuenta
        """
        querys = f'INSERT INTO cuentas(nombre_cuenta, contraseña, acceso) ' \
                 f'VALUES("{nombre_cuenta}", SHA("{contraseña}"),{acceso});'
        return self.bd.insertar(querys)

    def consultar_cuenta(self, usuario, contraseña):
        """
        Methodo Utilizado para poder gestionar si el usuario ha escrito bien sus contraseñas
        y pueda iniciar seccion
        """
        querys = f'SELECT * FROM cuentas WHERE nombre_cuenta = "{usuario}" AND contraseña = "{contraseña}";'
        datos = self.bd.consultar(querys)
        return datos

    def registrar_productos(self, objeto):
        """
        Methodo utilizado para gestionar registros de productos
        objeto es de tipo RegistroProductos()
        """
        objeto = her.recuperacion_sentencia(objeto)
        productos = RegistroProductos()
        productos.__dict__ = objeto.__dict__
        querys = '''
        INSERT INTO productos(nombre_producto, descripcion, cantidad, id_local)
        VALUES({}, {}, {}, {});
        '''.format(productos.nombre_producto, productos.descripcion, productos.cantidad, productos.id_local)
        return self.bd.insertar(querys)

    def registrar_empresas(self, objeto):
        """
        Methodo utilizado para gestionar registros de empresas
        objeto es tipo RegistroEmpresas()
        """
        objeto = her.recuperacion_sentencia(objeto)
        empresa = RegistroEmpresas()
        empresa.__dict__ = objeto.__dict__

        querys = '''
        INSERT INTO EMPRESAS(rut_empresa, nombre_empresa, giro_empresa, direccion_empresa, correo_empresa, 
        correo_respaldo, telefono_empresa, celular_empresa)
        VALUES({}, {}, {}, {}, {}, {}, {}, {});
        '''.format(empresa.rut_empresa, empresa.nombre_empresa, empresa.giro_empresa, empresa.direccion_empresa,
                   empresa.correo_empresa,
                   empresa.correo_respaldo, empresa.telefono_empresa, empresa.celular_empresa)
        return self.bd.insertar(querys)

    def registrar_personas_empresas(self, rut_empresa, rut_persona):
        """
        Methodo utilizado para gestionar empresas de usuarios
        este existe dado que un usuario puede participar en mas de una empresa
        """
        querys = f"INSERT INTO empresas_personas(rut_empresa, rut_persona) VALUES({rut_empresa}, {rut_persona});"
        return self.bd.insertar(querys)

    def registrar_departamento(self, objeto):
        """
        Methodo Utilizado para registrar departamentos
        """
        objeto = her.recuperacion_sentencia(objeto)
        obj = RegistrarDepartamento()
        obj.__dict__ = objeto.__dict__
        querys = """
        INSERT INTO departamentos (nombre_grupo, descripcion, id_local) 
        VALUES ({}, {}, {});
        """.format(obj.nombre_departamento, obj.descripcion, obj.id_local)
        return self.bd.insertar(querys)
    def registrar_personas(self, objeto):
        """
        Methodo utilizado para que gestione la creacion de usuarios nuevos
        comprobare si el correo existe, si no existe lo creara con default de password
        """
        personas = RegistroPersonas()
        personas.__dict__ = objeto.__dict__

        rut_existe = self.existe_persona(personas.rut_persona)

        if rut_existe.get("estado"):
            return {"estado": False, "condicion": "RUT_EXISTE"}

        apellido_antiguo = personas.apellidos
        contador = 0
        while True:
            nombre_cuenta = her.generar_nombres(personas.nombres, personas.apellidos, contador=contador)
            info = self.existe_cuenta(nombre_cuenta)
            if info.get("datos") is None:
                personas.apellidos = apellido_antiguo
                break
            contador += 1

        cuenta = self.registrar_cuenta(nombre_cuenta, "12345")

        if cuenta.get("estado"):
            personas = her.recuperacion_sentencia(personas)
            querys = '''
            INSERT INTO personas(rut_persona, nombres, apellidos, telefono, celular, correo, id_cuenta)
            VALUES({}, {}, {}, {}, {}, {}, {}); 
            '''.format(personas.rut_persona, personas.nombres, personas.apellidos, personas.telefono, personas.celular,
                       personas.correo, cuenta["ultimo_id"])
            self.bd.insertar(querys)
            self.registrar_personas_empresas(personas.rut_empresa, personas.rut_persona)
            return {"estado": True}
        return {"estado": False, "condicion": "REGISTRARCUENTA"}

    def registrar_estados(self, nombre):
        """
        Methodo Utilizado para ingresar los estados
        """
        querys = f'INSERT INTO estados(nombre_estado) VALUES("{nombre}")'
        self.bd.insertar(querys)

    def registrar_notas(self, objeto, cuenta, objetivo = "empresas"):
        """
        Methodo utilizado para gestionar notas de empresas y personas
        """
        nota = RegistroNotas()
        nota.__dict__ = her.recuperacion_sentencia(objeto).__dict__
        querys = '''
        INSERT INTO notas(nota, id_cuenta)
        VALUES({}, {});
        '''.format(nota.nota, cuenta.id_cuenta)
        nota_resgistrada = self.bd.insertar(querys)
        if not nota_resgistrada.get("estado"):
            return {"estado":False, "condicion": "INSERCION"}

        if objetivo == "empresas":
            querys = '''
                INSERT INTO empresas_notas(id_nota, rut_empresa)
                VALUES({},{});'''.format(nota_resgistrada.get("ultimo_id"), nota.rut_asociado)
            empresa_notas = self.bd.insertar(querys)
            if empresa_notas.get("estado"):
                return empresa_notas
            return {"estado":False, "condicion": "INSERCION"}
        elif objetivo == "personas":
            querys = '''
                INSERT INTO personas_notas(id_nota, rut_persona)
                VALUES({},{});
                '''.format(nota_resgistrada.get("ultimo_id"), nota.rut_asociado)
            persona_notas = self.bd.insertar(querys)

            if persona_notas.get("estado"):
                return persona_notas
            return {"estado":False, "condicion": "INSERCION"}

        return {"estado":False, "condicion":"SINSELECCION"}

    def registrar_estado_gastos(self, nombre):
        """
        Methodo utilizado para ingresar los estados de los gastos
        """
        querys = f'INSERT INTO estado_gastos(nombre) VALUES("{nombre}")'
        self.bd.insertar(querys)

    def lista_menu_empresas(self):
        """
        Methodo utilizado para gestionar menus de empresas
        """
        querys = "SELECT rut_empresa, nombre_empresa FROM empresas;"
        return self.bd.consultar(querys, all=True)

    def lista_menu_estados(self):
        """
        Methodo que gestiona estados de el programa
        """
        querys = f'SELECT id_estado, nombre_estado FROM estados;'
        return self.bd.consultar(querys, all=True)

    def lista_menu_personas(self):
        """
        Methodo utilizado para gstionar lista de personas
        """
        querys = "SELECT rut_persona, CONCAT(nombres, ' ', apellidos) as Nombres FROM personas;"
        return self.bd.consultar(querys, all=True)

    def lista_menu_locales(self):
        """
        Methodo Utilizado para gestionar menus de locales
        """
        querys = "SELECT id_local, nombre_local	FROM locales;"
        return self.bd.consultar(querys, all=True)

    def actualizar_grupo_usuario(self, correo, grupo):
        querys = f'UPDATE USUARIOS SET GRUPOS = {grupo} WHERE CORREO = "{correo}";'
        return self.bd.insertar(querys)

    def solicitar_estados(self):
        querys = f'SELECT * FROM ESTADOS;'
        return self.bd.consultar(querys, all=True)

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



    def solicitar_listado_servicios(self):
        querys = f'SELECT ID_SERVICIO, NOMBRE_SERVICIO FROM SERVICIOS;'
        return self.bd.consultar(querys, all=True)

    def nueva_contraseña(self, correo, contraseña_nueva):
        querys = f'UPDATE USUARIOS SET CONTRASEÑA = "{contraseña_nueva}" WHERE CORREO = "{correo}";'
        return self.bd.insertar(querys)

    def solicitar_lista_productos(self):
        querys = f'SELECT ID_PRODUCTO, NOMBRE_PRODUCTO, CANTIDAD FROM productos;'
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



    def listado_notas_empresa_especifica(self, contenido):
        querys = """
            SELECT n.id_nota, en.rut_empresa, n.nota, n.fecha_creacion, cu.nombre_cuenta
            FROM notas n
            INNER JOIN empresas_notas en
                ON en.id_nota = n.id_nota
            INNER JOIN cuentas cu
                ON cu.id_cuenta = n.id_cuenta
            WHERE en.rut_empresa = "{}"
            GROUP BY n.fecha_creacion DESC;
        """.format(contenido)
        datos = self.bd.consultar(querys, all=True)
        lista_notas = []
        for nota in datos.get("datos"):
            lista_notas.append(RegistroNotas(id_registro=nota[0], rut_asociado=nota[1],
                                             nota=nota[2], fecha_creacion=nota[3],
                                             id_cuenta=nota[4]))
        datos.update({"datos": lista_notas})
        return datos



    def asignar_grupo(self, rut_Trabajador, id_grupo):
        querys = """
        INSERT INTO grupos_trabajadores(ID_GRUPO, RUT_TRABAJADOR) 
        VALUES ('{}', '{}')
        """.format(id_grupo, rut_Trabajador)
        return self.bd.insertar(querys)
